from django.contrib import admin
from .models import Customer, Worker, Estimate, Job, Supplier, Material, Invoice, Payment


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'phone', 'city', 'created_at']
    list_filter = ['city', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering = ['-created_at']


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'worker_type', 'hourly_rate', 'experience_years', 'is_available']
    list_filter = ['worker_type', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'worker_type']
    ordering = ['user__first_name']


@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'estimated_cost', 'property_visit_date', 'estimate_sent_date']
    list_filter = ['status', 'property_visit_date', 'created_at']
    search_fields = ['customer__first_name', 'customer__last_name', 'work_description']
    ordering = ['-created_at']
    raw_id_fields = ['customer', 'created_by']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'job_title', 'customer', 'status', 'scheduled_start_date', 'scheduled_end_date']
    list_filter = ['status', 'scheduled_start_date', 'created_at']
    search_fields = ['job_title', 'customer__first_name', 'customer__last_name', 'description']
    ordering = ['scheduled_start_date']
    raw_id_fields = ['customer', 'managed_by', 'estimate']
    filter_horizontal = ['workers']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'contact_person', 'email', 'phone', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'contact_person', 'email']
    ordering = ['name']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'job', 'quantity', 'unit', 'unit_cost', 'total_cost', 'is_delivered']
    list_filter = ['is_delivered', 'order_date', 'expected_delivery_date']
    search_fields = ['name', 'job__job_title', 'supplier__name']
    ordering = ['-created_at']
    raw_id_fields = ['job', 'supplier']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'invoice_number', 'customer', 'status', 'total_amount', 'balance_due', 'invoice_date', 'due_date']
    list_filter = ['status', 'invoice_date', 'due_date']
    search_fields = ['invoice_number', 'customer__first_name', 'customer__last_name']
    ordering = ['-invoice_date']
    raw_id_fields = ['customer', 'job']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'invoice', 'amount', 'payment_method', 'payment_date', 'received_by']
    list_filter = ['payment_method', 'payment_date']
    search_fields = ['invoice__invoice_number', 'transaction_reference']
    ordering = ['-payment_date']
    raw_id_fields = ['invoice', 'received_by']
