from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from construction.models import (
    Customer, Worker, Estimate, Job, Supplier,
    Material, Invoice, Payment
)


class CustomerModelTest(TestCase):
    """Test cases for Customer model"""
    
    def setUp(self):
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
        """Test creating a customer"""
        customer = Customer.objects.create(**self.customer_data)
        self.assertEqual(customer.first_name, 'John')
        self.assertEqual(customer.last_name, 'Doe')
        self.assertEqual(customer.email, 'john.doe@example.com')
    
    def test_customer_full_name_property(self):
        """Test customer full_name property"""
        customer = Customer.objects.create(**self.customer_data)
        self.assertEqual(customer.full_name, 'John Doe')
    
    def test_customer_str_method(self):
        """Test customer string representation"""
        customer = Customer.objects.create(**self.customer_data)
        self.assertEqual(str(customer), 'John Doe')
    
    def test_email_uniqueness(self):
        """Test that email must be unique"""
        Customer.objects.create(**self.customer_data)
        with self.assertRaises(Exception):
            Customer.objects.create(**self.customer_data)


class EstimateModelTest(TestCase):
    """Test cases for Estimate model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='+254712345678',
            address='123 Main St',
            city='Nairobi',
            postal_code='00100'
        )
    
    def test_create_estimate(self):
        """Test creating an estimate"""
        estimate = Estimate.objects.create(
            customer=self.customer,
            created_by=self.user,
            work_description='Build new garage',
            estimated_cost=50000,
            estimated_duration_days=30,
            status='PENDING'
        )
        self.assertEqual(estimate.status, 'PENDING')
        self.assertEqual(estimate.customer, self.customer)
        self.assertEqual(estimate.created_by, self.user)
    
    def test_estimate_3_day_rule_within(self):
        """Test 3-day rule when within timeframe"""
        estimate = Estimate.objects.create(
            customer=self.customer,
            created_by=self.user,
            work_description='Build new garage',
            property_visit_date=date.today() - timedelta(days=2)
        )
        self.assertTrue(estimate.is_within_3_days_of_visit)
    
    def test_estimate_3_day_rule_exceeded(self):
        """Test 3-day rule when timeframe exceeded"""
        estimate = Estimate.objects.create(
            customer=self.customer,
            created_by=self.user,
            work_description='Build new garage',
            property_visit_date=date.today() - timedelta(days=4)
        )
        self.assertFalse(estimate.is_within_3_days_of_visit)
    
    def test_estimate_status_choices(self):
        """Test estimate can have different statuses"""
        statuses = ['PENDING', 'VISITED', 'SENT', 'ACCEPTED', 'REJECTED']
        for status_value in statuses:
            estimate = Estimate.objects.create(
                customer=self.customer,
                created_by=self.user,
                work_description='Test work',
                status=status_value
            )
            self.assertEqual(estimate.status, status_value)


class JobModelTest(TestCase):
    """Test cases for Job model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='manager',
            password='testpass123'
        )
        
        self.customer = Customer.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            phone='+254712345679',
            address='456 Oak Ave',
            city='Mombasa',
            postal_code='80100'
        )
        
        self.estimate = Estimate.objects.create(
            customer=self.customer,
            created_by=self.user,
            work_description='Kitchen renovation',
            estimated_cost=75000,
            status='ACCEPTED'
        )
        
        self.worker = Worker.objects.create(
            user=self.user,
            worker_type='CARPENTER',
            phone='+254712345680',
            hourly_rate=500,
            experience_years=5
        )
    
    def test_create_job(self):
        """Test creating a job"""
        job = Job.objects.create(
            estimate=self.estimate,
            customer=self.customer,
            managed_by=self.user,
            job_title='Kitchen Renovation',
            description='Complete kitchen renovation',
            scheduled_start_date=date.today() + timedelta(days=7),
            scheduled_end_date=date.today() + timedelta(days=37)
        )
        self.assertEqual(job.status, 'SCHEDULED')
        self.assertEqual(job.customer, self.customer)
    
    def test_job_needs_confirmation(self):
        """Test needs_confirmation property"""
        # Job starting in 3 days should need confirmation
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
        self.assertTrue(job.needs_confirmation)
    
    def test_assign_workers(self):
        """Test assigning workers to job"""
        job = Job.objects.create(
            estimate=self.estimate,
            customer=self.customer,
            managed_by=self.user,
            job_title='Test Job',
            description='Test',
            scheduled_start_date=date.today() + timedelta(days=7),
            scheduled_end_date=date.today() + timedelta(days=14)
        )
        job.workers.add(self.worker)
        self.assertEqual(job.workers.count(), 1)
        self.assertIn(self.worker, job.workers.all())


class InvoiceModelTest(TestCase):
    """Test cases for Invoice model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            password='testpass123'
        )
        
        self.customer = Customer.objects.create(
            first_name='Bob',
            last_name='Johnson',
            email='bob@example.com',
            phone='+254712345681',
            address='789 Pine St',
            city='Kisumu',
            postal_code='40100'
        )
        
        self.estimate = Estimate.objects.create(
            customer=self.customer,
            created_by=self.user,
            work_description='Bathroom renovation',
            estimated_cost=40000,
            status='ACCEPTED'
        )
        
        self.job = Job.objects.create(
            estimate=self.estimate,
            customer=self.customer,
            managed_by=self.user,
            job_title='Bathroom Renovation',
            description='Complete bathroom renovation',
            scheduled_start_date=date.today(),
            scheduled_end_date=date.today() + timedelta(days=14),
            status='COMPLETED'
        )
    
    def test_create_invoice(self):
        """Test creating an invoice"""
        invoice = Invoice.objects.create(
            job=self.job,
            customer=self.customer,
            labor_cost=25000,
            material_cost=15000,
            additional_costs=2000,
            tax_rate=16
        )
        self.assertIsNotNone(invoice.invoice_number)
        self.assertEqual(invoice.status, 'DRAFT')
    
    def test_invoice_number_auto_generation(self):
        """Test automatic invoice number generation"""
        invoice1 = Invoice.objects.create(
            job=self.job,
            customer=self.customer,
            labor_cost=1000
        )
        self.assertEqual(invoice1.invoice_number, 'INV-00001')
    
    def test_invoice_calculations(self):
        """Test invoice amount calculations"""
        invoice = Invoice.objects.create(
            job=self.job,
            customer=self.customer,
            labor_cost=10000,
            material_cost=5000,
            additional_costs=1000,
            tax_rate=16
        )
        
        self.assertEqual(invoice.subtotal, Decimal('16000'))
        self.assertEqual(invoice.tax_amount, Decimal('2560'))
        self.assertEqual(invoice.total_amount, Decimal('18560'))
    
    def test_invoice_due_date_auto_set(self):
        """Test that due date is automatically set to 30 days"""
        invoice = Invoice.objects.create(
            job=self.job,
            customer=self.customer,
            labor_cost=10000
        )
        expected_due_date = date.today() + timedelta(days=30)
        self.assertEqual(invoice.due_date, expected_due_date)
    
    def test_balance_due_calculation(self):
        """Test balance due calculation"""
        invoice = Invoice.objects.create(
            job=self.job,
            customer=self.customer,
            labor_cost=10000,
            material_cost=5000,
            tax_rate=0
        )
        
        # Initial balance should equal total
        self.assertEqual(invoice.balance_due, Decimal('15000'))
        
        # After partial payment
        invoice.amount_paid = Decimal('5000')
        invoice.save()
        self.assertEqual(invoice.balance_due, Decimal('10000'))


class PaymentModelTest(TestCase):
    """Test cases for Payment model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='cashier',
            password='testpass123'
        )
        
        self.customer = Customer.objects.create(
            first_name='Alice',
            last_name='Williams',
            email='alice@example.com',
            phone='+254712345682',
            address='321 Elm St',
            city='Nakuru',
            postal_code='20100'
        )
        
        self.estimate = Estimate.objects.create(
            customer=self.customer,
            created_by=self.user,
            work_description='Painting work',
            status='ACCEPTED'
        )
        
        self.job = Job.objects.create(
            estimate=self.estimate,
            customer=self.customer,
            managed_by=self.user,
            job_title='House Painting',
            description='Paint entire house',
            scheduled_start_date=date.today(),
            scheduled_end_date=date.today() + timedelta(days=7),
            status='COMPLETED'
        )
        
        self.invoice = Invoice.objects.create(
            job=self.job,
            customer=self.customer,
            labor_cost=20000,
            material_cost=10000,
            tax_rate=0
        )
    
    def test_create_payment(self):
        """Test creating a payment"""
        payment = Payment.objects.create(
            invoice=self.invoice,
            amount=10000,
            payment_method='CASH',
            received_by=self.user
        )
        self.assertEqual(payment.amount, Decimal('10000'))
        self.assertEqual(payment.payment_method, 'CASH')
    
    def test_payment_updates_invoice(self):
        """Test that payment updates invoice amount_paid"""
        initial_amount_paid = self.invoice.amount_paid
        
        payment = Payment.objects.create(
            invoice=self.invoice,
            amount=5000,
            payment_method='BANK_TRANSFER',
            received_by=self.user
        )
        
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.amount_paid, initial_amount_paid + Decimal('5000'))
    
    def test_full_payment_updates_invoice_status(self):
        """Test that full payment changes invoice status to PAID"""
        Payment.objects.create(
            invoice=self.invoice,
            amount=self.invoice.total_amount,
            payment_method='MOBILE_MONEY',
            received_by=self.user
        )
        
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, 'PAID')


class MaterialModelTest(TestCase):
    """Test cases for Material model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='manager',
            password='testpass123'
        )
        
        self.customer = Customer.objects.create(
            first_name='Tom',
            last_name='Brown',
            email='tom@example.com',
            phone='+254712345683',
            address='654 Maple Ave',
            city='Eldoret',
            postal_code='30100'
        )
        
        self.estimate = Estimate.objects.create(
            customer=self.customer,
            created_by=self.user,
            work_description='Wall construction',
            status='ACCEPTED'
        )
        
        self.job = Job.objects.create(
            estimate=self.estimate,
            customer=self.customer,
            managed_by=self.user,
            job_title='Wall Construction',
            description='Build boundary wall',
            scheduled_start_date=date.today() + timedelta(days=5),
            scheduled_end_date=date.today() + timedelta(days=20)
        )
        
        self.supplier = Supplier.objects.create(
            name='ABC Building Supplies',
            contact_person='John Supplier',
            email='john@abc.com',
            phone='+254712345684',
            address='Industrial Area'
        )
    
    def test_create_material(self):
        """Test creating a material"""
        material = Material.objects.create(
            job=self.job,
            supplier=self.supplier,
            name='Cement',
            quantity=50,
            unit='bags',
            unit_cost=650
        )
        self.assertEqual(material.name, 'Cement')
        self.assertEqual(material.quantity, Decimal('50'))
    
    def test_material_total_cost_calculation(self):
        """Test material total cost calculation"""
        material = Material.objects.create(
            job=self.job,
            supplier=self.supplier,
            name='Bricks',
            quantity=1000,
            unit='pieces',
            unit_cost=15
        )
        self.assertEqual(material.total_cost, Decimal('15000'))

