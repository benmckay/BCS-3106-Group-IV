from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date, timedelta
from construction.models import (
    Customer, Worker, Estimate, Job, Supplier,
    Material, Invoice, Payment
)


class Command(BaseCommand):
    help = 'Creates sample data for testing and demonstration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))

        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@bidii.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS(f'Created admin user: admin/admin123'))
        else:
            admin = User.objects.get(username='admin')
            self.stdout.write(self.style.WARNING('Admin user already exists'))

        # Create regular users for workers
        users = []
        worker_names = [
            ('john_mason', 'John', 'Mason'),
            ('mary_carpenter', 'Mary', 'Carpenter'),
            ('peter_plumber', 'Peter', 'Plumber'),
        ]
        
        for username, first, last in worker_names:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@bidii.com',
                    password='password123',
                    first_name=first,
                    last_name=last
                )
                users.append(user)
                self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
            else:
                users.append(User.objects.get(username=username))

        # Create customers
        customers_data = [
            {
                'first_name': 'James',
                'last_name': 'Kimani',
                'email': 'james.kimani@email.com',
                'phone': '+254712345678',
                'address': '123 Kenyatta Avenue',
                'city': 'Nairobi',
                'postal_code': '00100'
            },
            {
                'first_name': 'Sarah',
                'last_name': 'Wanjiru',
                'email': 'sarah.wanjiru@email.com',
                'phone': '+254723456789',
                'address': '456 Moi Avenue',
                'city': 'Mombasa',
                'postal_code': '80100'
            },
            {
                'first_name': 'David',
                'last_name': 'Odhiambo',
                'email': 'david.odhiambo@email.com',
                'phone': '+254734567890',
                'address': '789 Uhuru Highway',
                'city': 'Kisumu',
                'postal_code': '40100'
            },
            {
                'first_name': 'Grace',
                'last_name': 'Mutua',
                'email': 'grace.mutua@email.com',
                'phone': '+254745678901',
                'address': '321 Dedan Kimathi Street',
                'city': 'Nakuru',
                'postal_code': '20100'
            }
        ]

        customers = []
        for data in customers_data:
            customer, created = Customer.objects.get_or_create(
                email=data['email'],
                defaults=data
            )
            customers.append(customer)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created customer: {customer.full_name}'))

        # Create workers
        workers_data = [
            {
                'user': users[0] if len(users) > 0 else admin,
                'worker_type': 'BRICKLAYER',
                'phone': '+254756789012',
                'hourly_rate': 500,
                'experience_years': 8,
                'is_available': True
            },
            {
                'user': users[1] if len(users) > 1 else admin,
                'worker_type': 'CARPENTER',
                'phone': '+254767890123',
                'hourly_rate': 600,
                'experience_years': 6,
                'is_available': True
            },
            {
                'user': users[2] if len(users) > 2 else admin,
                'worker_type': 'PLUMBER',
                'phone': '+254778901234',
                'hourly_rate': 550,
                'experience_years': 5,
                'is_available': False
            }
        ]

        workers = []
        for data in workers_data:
            worker, created = Worker.objects.get_or_create(
                user=data['user'],
                defaults=data
            )
            workers.append(worker)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created worker: {worker}'))

        # Create suppliers
        suppliers_data = [
            {
                'name': 'ABC Building Supplies',
                'contact_person': 'John Supplier',
                'email': 'john@abc-supplies.co.ke',
                'phone': '+254789012345',
                'address': 'Industrial Area, Nairobi',
                'website': 'https://abc-supplies.co.ke',
                'is_active': True
            },
            {
                'name': 'Quality Materials Ltd',
                'contact_person': 'Jane Materials',
                'email': 'jane@quality-materials.co.ke',
                'phone': '+254790123456',
                'address': 'Mombasa Road, Nairobi',
                'website': 'https://quality-materials.co.ke',
                'is_active': True
            }
        ]

        suppliers = []
        for data in suppliers_data:
            supplier, created = Supplier.objects.get_or_create(
                email=data['email'],
                defaults=data
            )
            suppliers.append(supplier)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created supplier: {supplier.name}'))

        # Create estimates
        estimates_data = [
            {
                'customer': customers[0],
                'created_by': admin,
                'work_description': 'Build new boundary wall and gate',
                'property_visit_date': date.today() - timedelta(days=5),
                'detailed_work_description': 'Construct 50-meter concrete boundary wall with steel gate',
                'estimated_cost': 350000,
                'estimated_duration_days': 21,
                'status': 'ACCEPTED',
                'estimate_sent_date': date.today() - timedelta(days=3),
                'response_date': date.today() - timedelta(days=1)
            },
            {
                'customer': customers[1],
                'created_by': admin,
                'work_description': 'Kitchen renovation',
                'property_visit_date': date.today() - timedelta(days=2),
                'detailed_work_description': 'Complete kitchen renovation including cabinets and plumbing',
                'estimated_cost': 180000,
                'estimated_duration_days': 14,
                'status': 'SENT',
                'estimate_sent_date': date.today() - timedelta(days=1)
            },
            {
                'customer': customers[2],
                'created_by': admin,
                'work_description': 'Bathroom addition',
                'property_visit_date': date.today() + timedelta(days=2),
                'status': 'PENDING'
            }
        ]

        estimates = []
        for i, data in enumerate(estimates_data):
            estimate, created = Estimate.objects.get_or_create(
                customer=data['customer'],
                work_description=data['work_description'],
                defaults=data
            )
            estimates.append(estimate)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created estimate #{estimate.id}'))

        # Create jobs for accepted estimates
        if estimates[0].status == 'ACCEPTED':
            job_data = {
                'estimate': estimates[0],
                'customer': estimates[0].customer,
                'managed_by': admin,
                'job_title': 'Boundary Wall Construction',
                'description': estimates[0].detailed_work_description,
                'scheduled_start_date': date.today() + timedelta(days=7),
                'scheduled_end_date': date.today() + timedelta(days=28),
                'status': 'SCHEDULED'
            }
            
            job, created = Job.objects.get_or_create(
                estimate=estimates[0],
                defaults=job_data
            )
            if created:
                # Assign workers
                job.workers.add(workers[0], workers[1])
                self.stdout.write(self.style.SUCCESS(f'Created job: {job.job_title}'))
                
                # Create materials for the job
                materials_data = [
                    {
                        'job': job,
                        'supplier': suppliers[0],
                        'name': 'Cement',
                        'description': 'High-grade cement',
                        'quantity': 100,
                        'unit': 'bags',
                        'unit_cost': 650,
                        'order_date': date.today(),
                        'expected_delivery_date': date.today() + timedelta(days=6),
                        'is_delivered': False
                    },
                    {
                        'job': job,
                        'supplier': suppliers[0],
                        'name': 'Bricks',
                        'description': 'Standard building bricks',
                        'quantity': 5000,
                        'unit': 'pieces',
                        'unit_cost': 15,
                        'order_date': date.today(),
                        'expected_delivery_date': date.today() + timedelta(days=6),
                        'is_delivered': False
                    },
                    {
                        'job': job,
                        'supplier': suppliers[1],
                        'name': 'Steel Bars',
                        'description': '12mm steel reinforcement bars',
                        'quantity': 50,
                        'unit': 'pieces',
                        'unit_cost': 800,
                        'order_date': date.today(),
                        'expected_delivery_date': date.today() + timedelta(days=6),
                        'is_delivered': False
                    }
                ]
                
                for mat_data in materials_data:
                    material, mat_created = Material.objects.get_or_create(
                        job=job,
                        name=mat_data['name'],
                        defaults=mat_data
                    )
                    if mat_created:
                        self.stdout.write(self.style.SUCCESS(f'Created material: {material.name}'))

        # Create a completed job with invoice
        completed_estimate_data = {
            'customer': customers[3],
            'created_by': admin,
            'work_description': 'House painting',
            'property_visit_date': date.today() - timedelta(days=45),
            'detailed_work_description': 'Complete exterior and interior house painting',
            'estimated_cost': 120000,
            'estimated_duration_days': 10,
            'status': 'ACCEPTED',
            'estimate_sent_date': date.today() - timedelta(days=43),
            'response_date': date.today() - timedelta(days=40)
        }
        
        completed_estimate, created = Estimate.objects.get_or_create(
            customer=customers[3],
            work_description='House painting',
            defaults=completed_estimate_data
        )
        
        if created or not hasattr(completed_estimate, 'job'):
            completed_job_data = {
                'estimate': completed_estimate,
                'customer': completed_estimate.customer,
                'managed_by': admin,
                'job_title': 'House Painting Project',
                'description': completed_estimate.detailed_work_description,
                'scheduled_start_date': date.today() - timedelta(days=35),
                'scheduled_end_date': date.today() - timedelta(days=25),
                'actual_start_date': date.today() - timedelta(days=35),
                'actual_end_date': date.today() - timedelta(days=26),
                'status': 'COMPLETED',
                'confirmation_date': date.today() - timedelta(days=37)
            }
            
            completed_job, job_created = Job.objects.get_or_create(
                estimate=completed_estimate,
                defaults=completed_job_data
            )
            
            if job_created:
                completed_job.workers.add(workers[0])
                self.stdout.write(self.style.SUCCESS(f'Created completed job: {completed_job.job_title}'))
                
                # Create invoice
                invoice_data = {
                    'job': completed_job,
                    'customer': completed_job.customer,
                    'labor_cost': 80000,
                    'material_cost': 35000,
                    'additional_costs': 5000,
                    'tax_rate': 16,
                    'status': 'SENT'
                }
                
                invoice, inv_created = Invoice.objects.get_or_create(
                    job=completed_job,
                    defaults=invoice_data
                )
                
                if inv_created:
                    self.stdout.write(self.style.SUCCESS(f'Created invoice: {invoice.invoice_number}'))
                    
                    # Create partial payment
                    payment_data = {
                        'invoice': invoice,
                        'amount': 70000,
                        'payment_method': 'BANK_TRANSFER',
                        'payment_date': date.today() - timedelta(days=10),
                        'transaction_reference': 'TXN-2025-001',
                        'received_by': admin
                    }
                    
                    payment, pay_created = Payment.objects.get_or_create(
                        invoice=invoice,
                        transaction_reference='TXN-2025-001',
                        defaults=payment_data
                    )
                    
                    if pay_created:
                        self.stdout.write(self.style.SUCCESS(f'Created payment: KES {payment.amount}'))

        self.stdout.write(self.style.SUCCESS('\n=== Sample Data Creation Complete! ==='))
        self.stdout.write(self.style.SUCCESS('\nSummary:'))
        self.stdout.write(f'  Customers: {Customer.objects.count()}')
        self.stdout.write(f'  Workers: {Worker.objects.count()}')
        self.stdout.write(f'  Estimates: {Estimate.objects.count()}')
        self.stdout.write(f'  Jobs: {Job.objects.count()}')
        self.stdout.write(f'  Suppliers: {Supplier.objects.count()}')
        self.stdout.write(f'  Materials: {Material.objects.count()}')
        self.stdout.write(f'  Invoices: {Invoice.objects.count()}')
        self.stdout.write(f'  Payments: {Payment.objects.count()}')
        self.stdout.write(self.style.SUCCESS('\nYou can now login with:'))
        self.stdout.write('  Username: admin')
        self.stdout.write('  Password: admin123')

