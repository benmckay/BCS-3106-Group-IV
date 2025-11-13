from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from datetime import date, timedelta

from construction.models import Customer, Worker, Estimate, Job, Invoice


class AuthenticationAPITest(APITestCase):
    """Test cases for authentication endpoints"""
    
    def test_user_registration(self):
        """Test user registration endpoint"""
        url = '/api/auth/register/'
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
    
    def test_user_login(self):
        """Test user login endpoint"""
        # Create user first
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Attempt login
        url = '/api/auth/login/'
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials"""
        url = '/api/auth/login/'
        data = {
            'username': 'nonexistent',
            'password': 'wrongpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_protected_endpoint_without_auth(self):
        """Test accessing protected endpoint without authentication"""
        url = '/api/customers/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CustomerAPITest(APITestCase):
    """Test cases for Customer API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.customer_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '+254712345678',
            'address': '123 Main Street',
            'city': 'Nairobi',
            'postal_code': '00100'
        }
    
    def test_create_customer(self):
        """Test creating a customer via API"""
        url = '/api/customers/'
        response = self.client.post(url, self.customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['email'], 'john.doe@example.com')
    
    def test_list_customers(self):
        """Test listing customers"""
        # Create some customers
        Customer.objects.create(**self.customer_data)
        
        url = '/api/customers/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
    
    def test_retrieve_customer(self):
        """Test retrieving a specific customer"""
        customer = Customer.objects.create(**self.customer_data)
        
        url = f'/api/customers/{customer.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], customer.id)
    
    def test_update_customer(self):
        """Test updating a customer"""
        customer = Customer.objects.create(**self.customer_data)
        
        url = f'/api/customers/{customer.id}/'
        updated_data = self.customer_data.copy()
        updated_data['phone'] = '+254799999999'
        
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '+254799999999')
    
    def test_delete_customer(self):
        """Test deleting a customer"""
        customer = Customer.objects.create(**self.customer_data)
        
        url = f'/api/customers/{customer.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify customer is deleted
        self.assertFalse(Customer.objects.filter(id=customer.id).exists())
    
    def test_search_customers(self):
        """Test searching customers"""
        Customer.objects.create(**self.customer_data)
        
        url = '/api/customers/?search=John'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)


class EstimateAPITest(APITestCase):
    """Test cases for Estimate API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='manager',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.customer = Customer.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            phone='+254712345679',
            address='456 Oak Ave',
            city='Mombasa',
            postal_code='80100'
        )
    
    def test_create_estimate(self):
        """Test creating an estimate via API"""
        url = '/api/estimates/'
        data = {
            'customer_id': self.customer.id,
            'work_description': 'Build new garage',
            'estimated_cost': 50000,
            'estimated_duration_days': 30
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'PENDING')
    
    def test_update_estimate_status(self):
        """Test updating estimate status"""
        estimate = Estimate.objects.create(
            customer=self.customer,
            created_by=self.user,
            work_description='Kitchen renovation',
            status='PENDING'
        )
        
        url = f'/api/estimates/{estimate.id}/'
        data = {
            'customer_id': self.customer.id,
            'work_description': 'Kitchen renovation',
            'status': 'VISITED',
            'property_visit_date': date.today().isoformat()
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'VISITED')
    
    def test_list_pending_estimates(self):
        """Test listing pending estimates"""
        Estimate.objects.create(
            customer=self.customer,
            created_by=self.user,
            work_description='Test work',
            status='PENDING'
        )
        
        url = '/api/estimates/pending_visits/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class JobAPITest(APITestCase):
    """Test cases for Job API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='supervisor',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.customer = Customer.objects.create(
            first_name='Bob',
            last_name='Johnson',
            email='bob@example.com',
            phone='+254712345680',
            address='789 Pine St',
            city='Kisumu',
            postal_code='40100'
        )
        
        self.estimate = Estimate.objects.create(
            customer=self.customer,
            created_by=self.user,
            work_description='Bathroom renovation',
            status='ACCEPTED'
        )
        
        self.worker = Worker.objects.create(
            user=self.user,
            worker_type='PLUMBER',
            phone='+254712345681',
            hourly_rate=600,
            experience_years=7
        )
    
    def test_create_job(self):
        """Test creating a job via API"""
        url = '/api/jobs/'
        data = {
            'estimate_id': self.estimate.id,
            'customer_id': self.customer.id,
            'job_title': 'Bathroom Renovation',
            'description': 'Complete bathroom renovation',
            'scheduled_start_date': (date.today() + timedelta(days=7)).isoformat(),
            'scheduled_end_date': (date.today() + timedelta(days=21)).isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'SCHEDULED')
    
    def test_confirm_job(self):
        """Test confirming a job"""
        job = Job.objects.create(
            estimate=self.estimate,
            customer=self.customer,
            managed_by=self.user,
            job_title='Test Job',
            description='Test',
            scheduled_start_date=date.today() + timedelta(days=3),
            scheduled_end_date=date.today() + timedelta(days=10),
            status='SCHEDULED'
        )
        
        url = f'/api/jobs/{job.id}/confirm/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'CONFIRMED')
    
    def test_start_job(self):
        """Test starting a job"""
        job = Job.objects.create(
            estimate=self.estimate,
            customer=self.customer,
            managed_by=self.user,
            job_title='Test Job',
            description='Test',
            scheduled_start_date=date.today(),
            scheduled_end_date=date.today() + timedelta(days=7),
            status='CONFIRMED'
        )
        
        url = f'/api/jobs/{job.id}/start/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'IN_PROGRESS')
    
    def test_complete_job(self):
        """Test completing a job"""
        job = Job.objects.create(
            estimate=self.estimate,
            customer=self.customer,
            managed_by=self.user,
            job_title='Test Job',
            description='Test',
            scheduled_start_date=date.today() - timedelta(days=7),
            scheduled_end_date=date.today(),
            status='IN_PROGRESS'
        )
        
        url = f'/api/jobs/{job.id}/complete/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'COMPLETED')
    
    def test_list_upcoming_jobs(self):
        """Test listing upcoming jobs"""
        Job.objects.create(
            estimate=self.estimate,
            customer=self.customer,
            managed_by=self.user,
            job_title='Future Job',
            description='Test',
            scheduled_start_date=date.today() + timedelta(days=10),
            scheduled_end_date=date.today() + timedelta(days=20),
            status='SCHEDULED'
        )
        
        url = '/api/jobs/upcoming/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DashboardAPITest(APITestCase):
    """Test cases for Dashboard API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_dashboard_stats(self):
        """Test dashboard statistics endpoint"""
        url = '/api/dashboard/stats/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('customers', response.data)
        self.assertIn('jobs', response.data)
        self.assertIn('invoices', response.data)
    
    def test_dashboard_charts(self):
        """Test dashboard charts endpoint"""
        url = '/api/dashboard/charts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Charts may not be generated if no data exists
        self.assertIsInstance(response.data, dict)

