from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from .models import (
    Customer, Worker, Estimate, Job, Supplier, 
    Material, Invoice, Payment
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name']
        read_only_fields = ['id']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model"""
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_email(self, value):
        """Ensure email is unique (case-insensitive)"""
        if Customer.objects.filter(email__iexact=value).exists():
            if self.instance and self.instance.email.lower() == value.lower():
                return value
            raise serializers.ValidationError("A customer with this email already exists.")
        return value


class WorkerSerializer(serializers.ModelSerializer):
    """Serializer for Worker model"""
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='user', 
        write_only=True
    )
    worker_type_display = serializers.CharField(source='get_worker_type_display', read_only=True)
    
    class Meta:
        model = Worker
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class EstimateSerializer(serializers.ModelSerializer):
    """Serializer for Estimate model"""
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source='customer',
        write_only=True
    )
    created_by = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_within_3_days_of_visit = serializers.ReadOnlyField()
    
    class Meta:
        model = Estimate
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'initial_contact_date']
    
    def validate(self, attrs):
        """Validate estimate data"""
        if attrs.get('status') == 'SENT' and not attrs.get('estimate_sent_date'):
            attrs['estimate_sent_date'] = timezone.now().date()
        
        if attrs.get('status') in ['ACCEPTED', 'REJECTED'] and not attrs.get('response_date'):
            attrs['response_date'] = timezone.now().date()
        
        return attrs


class MaterialSerializer(serializers.ModelSerializer):
    """Serializer for Material model"""
    supplier = serializers.StringRelatedField(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        source='supplier',
        write_only=True,
        allow_null=True,
        required=False
    )
    total_cost = serializers.ReadOnlyField()
    
    class Meta:
        model = Material
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class JobSerializer(serializers.ModelSerializer):
    """Serializer for Job model"""
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source='customer',
        write_only=True
    )
    estimate = EstimateSerializer(read_only=True)
    estimate_id = serializers.PrimaryKeyRelatedField(
        queryset=Estimate.objects.all(),
        source='estimate',
        write_only=True
    )
    managed_by = UserSerializer(read_only=True)
    workers = WorkerSerializer(many=True, read_only=True)
    worker_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Worker.objects.all(),
        source='workers',
        write_only=True,
        required=False
    )
    materials = MaterialSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    needs_confirmation = serializers.ReadOnlyField()
    total_material_cost = serializers.ReadOnlyField()
    
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        """Validate job dates"""
        scheduled_start = attrs.get('scheduled_start_date')
        scheduled_end = attrs.get('scheduled_end_date')
        
        if scheduled_start and scheduled_end and scheduled_end < scheduled_start:
            raise serializers.ValidationError(
                "Scheduled end date must be after or equal to start date."
            )
        
        actual_start = attrs.get('actual_start_date')
        actual_end = attrs.get('actual_end_date')
        
        if actual_start and actual_end and actual_end < actual_start:
            raise serializers.ValidationError(
                "Actual end date must be after or equal to start date."
            )
        
        return attrs


class SupplierSerializer(serializers.ModelSerializer):
    """Serializer for Supplier model"""
    
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model"""
    invoice = serializers.StringRelatedField(read_only=True)
    invoice_id = serializers.PrimaryKeyRelatedField(
        queryset=Invoice.objects.all(),
        source='invoice',
        write_only=True
    )
    received_by = UserSerializer(read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_amount(self, value):
        """Ensure payment amount is valid"""
        if value <= 0:
            raise serializers.ValidationError("Payment amount must be greater than zero.")
        return value


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for Invoice model"""
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source='customer',
        write_only=True
    )
    job = JobSerializer(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(),
        source='job',
        write_only=True
    )
    payments = PaymentSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    # Calculated fields
    subtotal = serializers.ReadOnlyField()
    tax_amount = serializers.ReadOnlyField()
    total_amount = serializers.ReadOnlyField()
    balance_due = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'invoice_date', 'amount_paid']
    
    def validate(self, attrs):
        """Validate invoice data"""
        if attrs.get('amount_paid', 0) < 0:
            raise serializers.ValidationError("Amount paid cannot be negative.")
        
        return attrs


# Nested serializers for detailed views
class JobDetailSerializer(JobSerializer):
    """Detailed serializer for Job with all related data"""
    materials = MaterialSerializer(many=True, read_only=True)


class InvoiceDetailSerializer(InvoiceSerializer):
    """Detailed serializer for Invoice with all related data"""
    job = JobDetailSerializer(read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)


class CustomerDetailSerializer(CustomerSerializer):
    """Detailed serializer for Customer with related estimates and jobs"""
    estimates = EstimateSerializer(many=True, read_only=True)
    jobs = JobSerializer(many=True, read_only=True)
    invoices = InvoiceSerializer(many=True, read_only=True)

