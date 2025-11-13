from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta


class Customer(models.Model):
    """Model representing a customer"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Worker(models.Model):
    """Model representing a skilled worker"""
    WORKER_TYPES = [
        ('BRICKLAYER', 'Bricklayer'),
        ('CARPENTER', 'Carpenter'),
        ('PLUMBER', 'Plumber'),
        ('ELECTRICIAN', 'Electrician'),
        ('PAINTER', 'Painter'),
        ('GENERAL', 'General Worker'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker_profile')
    worker_type = models.CharField(max_length=20, choices=WORKER_TYPES)
    phone = models.CharField(max_length=20)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    experience_years = models.IntegerField(validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['worker_type', 'user__first_name']
        verbose_name = 'Worker'
        verbose_name_plural = 'Workers'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_worker_type_display()}"


class Estimate(models.Model):
    """Model representing a cost estimate for a job"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending Visit'),
        ('VISITED', 'Property Visited'),
        ('SENT', 'Estimate Sent'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='estimates')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='estimates_created')
    
    # Contact and initial info
    initial_contact_date = models.DateTimeField(auto_now_add=True)
    work_description = models.TextField(help_text="Initial outline of proposed work")
    
    # Property visit
    property_visit_date = models.DateField(null=True, blank=True)
    detailed_work_description = models.TextField(blank=True, help_text="Detailed description after property visit")
    
    # Estimate details
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    estimated_duration_days = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    
    # Status and dates
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    estimate_sent_date = models.DateField(null=True, blank=True)
    response_date = models.DateField(null=True, blank=True)
    
    # Additional info
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Estimate'
        verbose_name_plural = 'Estimates'
    
    def __str__(self):
        return f"Estimate #{self.id} - {self.customer.full_name} - {self.get_status_display()}"
    
    @property
    def is_within_3_days_of_visit(self):
        """Check if estimate should be sent within 3 days of visit"""
        if self.property_visit_date:
            deadline = self.property_visit_date + timedelta(days=3)
            return timezone.now().date() <= deadline
        return False


class Job(models.Model):
    """Model representing a scheduled building job"""
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('CONFIRMED', 'Confirmed'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    estimate = models.OneToOneField(Estimate, on_delete=models.CASCADE, related_name='job')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='jobs')
    managed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='jobs_managed')
    
    # Job details
    job_title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Scheduling
    scheduled_start_date = models.DateField()
    scheduled_end_date = models.DateField()
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    confirmation_date = models.DateField(null=True, blank=True, help_text="Date when customer confirmed start date")
    
    # Workers assigned
    workers = models.ManyToManyField(Worker, related_name='jobs', blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scheduled_start_date']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
    
    def __str__(self):
        return f"Job #{self.id} - {self.job_title} - {self.customer.full_name}"
    
    @property
    def needs_confirmation(self):
        """Check if job needs customer confirmation (few days before start)"""
        if self.scheduled_start_date and self.status == 'SCHEDULED':
            days_until_start = (self.scheduled_start_date - timezone.now().date()).days
            return 1 <= days_until_start <= 5  # 1-5 days before
        return False
    
    @property
    def total_material_cost(self):
        """Calculate total cost of all materials for this job"""
        return sum(material.total_cost for material in self.materials.all())


class Supplier(models.Model):
    """Model representing a building materials supplier"""
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
    
    def __str__(self):
        return self.name


class Material(models.Model):
    """Model representing building materials for a job"""
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='materials')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='materials_supplied')
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=50, help_text="e.g., kg, m, pieces, bags")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Ordering
    order_date = models.DateField(null=True, blank=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    actual_delivery_date = models.DateField(null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['job', 'name']
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'
    
    def __str__(self):
        return f"{self.name} - {self.quantity} {self.unit}"
    
    @property
    def total_cost(self):
        """Calculate total cost for this material"""
        return self.quantity * self.unit_cost


class Invoice(models.Model):
    """Model representing an invoice for a completed job"""
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SENT', 'Sent'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name='invoice')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(help_text="Customer has 30 days to pay")
    
    # Costs
    labor_cost = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    material_cost = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    additional_costs = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    
    # Payment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-invoice_date']
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
    
    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.customer.full_name}"
    
    def save(self, *args, **kwargs):
        # Auto-generate invoice number if not set
        if not self.invoice_number:
            last_invoice = Invoice.objects.order_by('-id').first()
            if last_invoice:
                last_number = int(last_invoice.invoice_number.split('-')[-1])
                self.invoice_number = f"INV-{last_number + 1:05d}"
            else:
                self.invoice_number = "INV-00001"
        
        # Set due date if not set (30 days from invoice date)
        if not self.due_date:
            self.due_date = timezone.now().date() + timedelta(days=30)
        
        super().save(*args, **kwargs)
    
    @property
    def subtotal(self):
        """Calculate subtotal before tax"""
        return self.labor_cost + self.material_cost + self.additional_costs
    
    @property
    def tax_amount(self):
        """Calculate tax amount"""
        return (self.subtotal * self.tax_rate) / 100
    
    @property
    def total_amount(self):
        """Calculate total amount including tax"""
        from decimal import Decimal
        result = self.subtotal + self.tax_amount
        return Decimal(str(result))
    
    @property
    def balance_due(self):
        """Calculate remaining balance"""
        from decimal import Decimal
        result = self.total_amount - self.amount_paid
        return Decimal(str(result))
    
    @property
    def is_overdue(self):
        """Check if invoice is overdue"""
        if self.status in ['SENT', 'OVERDUE'] and self.due_date:
            return timezone.now().date() > self.due_date
        return False


class Payment(models.Model):
    """Model representing a payment made against an invoice"""
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('CHEQUE', 'Cheque'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('MOBILE_MONEY', 'Mobile Money'),
    ]
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_date = models.DateField(default=timezone.now)
    transaction_reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='payments_received')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-payment_date']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
    
    def __str__(self):
        return f"Payment of ${self.amount} for Invoice #{self.invoice.invoice_number}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update invoice amount paid
        self.invoice.amount_paid = sum(
            payment.amount for payment in self.invoice.payments.all()
        )
        if self.invoice.amount_paid >= self.invoice.total_amount:
            self.invoice.status = 'PAID'
        self.invoice.save()
