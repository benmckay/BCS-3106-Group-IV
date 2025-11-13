from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum, Count, Q, Avg
from datetime import timedelta
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

from .models import (
    Customer, Worker, Estimate, Job, Supplier,
    Material, Invoice, Payment
)
from .serializers import (
    UserSerializer, UserRegistrationSerializer,
    CustomerSerializer, CustomerDetailSerializer,
    WorkerSerializer, EstimateSerializer, JobSerializer,
    JobDetailSerializer, SupplierSerializer, MaterialSerializer,
    InvoiceSerializer, InvoiceDetailSerializer, PaymentSerializer
)


# Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Get current logged-in user details"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# ViewSets
class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Customer CRUD operations
    Provides list, create, retrieve, update, and delete operations
    """
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'city']
    ordering_fields = ['created_at', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CustomerDetailSerializer
        return CustomerSerializer
    
    @action(detail=True, methods=['get'])
    def estimates(self, request, pk=None):
        """Get all estimates for a specific customer"""
        customer = self.get_object()
        estimates = customer.estimates.all()
        serializer = EstimateSerializer(estimates, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def jobs(self, request, pk=None):
        """Get all jobs for a specific customer"""
        customer = self.get_object()
        jobs = customer.jobs.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


class WorkerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Worker CRUD operations
    """
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['worker_type', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'worker_type']
    ordering_fields = ['created_at', 'hourly_rate', 'experience_years']
    ordering = ['user__first_name']
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available workers"""
        workers = self.queryset.filter(is_available=True)
        serializer = self.get_serializer(workers, many=True)
        return Response(serializer.data)


class EstimateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Estimate CRUD operations
    """
    queryset = Estimate.objects.all()
    serializer_class = EstimateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'customer']
    search_fields = ['customer__first_name', 'customer__last_name', 'work_description']
    ordering_fields = ['created_at', 'property_visit_date', 'estimated_cost']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """Set the created_by field to the current user"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def pending_visits(self, request):
        """Get estimates pending property visit"""
        estimates = self.queryset.filter(status='PENDING')
        serializer = self.get_serializer(estimates, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def accepted(self, request):
        """Get accepted estimates ready for job scheduling"""
        estimates = self.queryset.filter(status='ACCEPTED')
        serializer = self.get_serializer(estimates, many=True)
        return Response(serializer.data)


class JobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Job CRUD operations
    """
    queryset = Job.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'customer']
    search_fields = ['job_title', 'description', 'customer__first_name', 'customer__last_name']
    ordering_fields = ['scheduled_start_date', 'scheduled_end_date', 'created_at']
    ordering = ['scheduled_start_date']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return JobDetailSerializer
        return JobSerializer
    
    def perform_create(self, serializer):
        """Set the managed_by field to the current user"""
        serializer.save(managed_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming jobs"""
        upcoming_jobs = self.queryset.filter(
            scheduled_start_date__gte=timezone.now().date(),
            status__in=['SCHEDULED', 'CONFIRMED']
        )
        serializer = self.get_serializer(upcoming_jobs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def in_progress(self, request):
        """Get jobs currently in progress"""
        in_progress_jobs = self.queryset.filter(status='IN_PROGRESS')
        serializer = self.get_serializer(in_progress_jobs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def needs_confirmation(self, request):
        """Get jobs that need customer confirmation"""
        today = timezone.now().date()
        confirmation_window = today + timedelta(days=5)
        jobs = self.queryset.filter(
            scheduled_start_date__range=[today + timedelta(days=1), confirmation_window],
            status='SCHEDULED'
        )
        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a job start date"""
        job = self.get_object()
        job.status = 'CONFIRMED'
        job.confirmation_date = timezone.now().date()
        job.save()
        serializer = self.get_serializer(job)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start a job"""
        job = self.get_object()
        job.status = 'IN_PROGRESS'
        job.actual_start_date = timezone.now().date()
        job.save()
        serializer = self.get_serializer(job)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete a job"""
        job = self.get_object()
        job.status = 'COMPLETED'
        job.actual_end_date = timezone.now().date()
        job.save()
        serializer = self.get_serializer(job)
        return Response(serializer.data)


class SupplierViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Supplier CRUD operations
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'contact_person', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class MaterialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Material CRUD operations
    """
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['job', 'supplier', 'is_delivered']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'order_date', 'expected_delivery_date']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def pending_delivery(self, request):
        """Get materials pending delivery"""
        materials = self.queryset.filter(is_delivered=False, order_date__isnull=False)
        serializer = self.get_serializer(materials, many=True)
        return Response(serializer.data)


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Invoice CRUD operations
    """
    queryset = Invoice.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'customer']
    search_fields = ['invoice_number', 'customer__first_name', 'customer__last_name']
    ordering_fields = ['invoice_date', 'due_date', 'created_at']
    ordering = ['-invoice_date']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return InvoiceDetailSerializer
        return InvoiceSerializer
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue invoices"""
        today = timezone.now().date()
        overdue_invoices = self.queryset.filter(
            Q(status='SENT') | Q(status='OVERDUE'),
            due_date__lt=today
        )
        # Update status to overdue
        overdue_invoices.update(status='OVERDUE')
        serializer = self.get_serializer(overdue_invoices, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unpaid(self, request):
        """Get all unpaid invoices"""
        unpaid_invoices = self.queryset.filter(status__in=['SENT', 'OVERDUE'])
        serializer = self.get_serializer(unpaid_invoices, many=True)
        return Response(serializer.data)


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Payment CRUD operations
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['invoice', 'payment_method']
    search_fields = ['transaction_reference', 'invoice__invoice_number']
    ordering_fields = ['payment_date', 'amount', 'created_at']
    ordering = ['-payment_date']
    
    def perform_create(self, serializer):
        """Set the received_by field to the current user"""
        serializer.save(received_by=self.request.user)


# Dashboard and Analytics Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics for the construction management system
    """
    today = timezone.now().date()
    
    # Customer stats
    total_customers = Customer.objects.count()
    
    # Job stats
    total_jobs = Job.objects.count()
    active_jobs = Job.objects.filter(status='IN_PROGRESS').count()
    scheduled_jobs = Job.objects.filter(status__in=['SCHEDULED', 'CONFIRMED']).count()
    completed_jobs = Job.objects.filter(status='COMPLETED').count()
    
    # Estimate stats
    pending_estimates = Estimate.objects.filter(status='PENDING').count()
    accepted_estimates = Estimate.objects.filter(status='ACCEPTED').count()
    
    # Invoice stats
    total_invoices = Invoice.objects.count()
    paid_invoices = Invoice.objects.filter(status='PAID').count()
    overdue_invoices = Invoice.objects.filter(
        Q(status='SENT') | Q(status='OVERDUE'),
        due_date__lt=today
    ).count()
    
    # Revenue stats
    total_revenue = Invoice.objects.filter(status='PAID').aggregate(
        total=Sum('amount_paid')
    )['total'] or 0
    
    pending_revenue = Invoice.objects.filter(status__in=['SENT', 'OVERDUE']).aggregate(
        total=Sum('labor_cost') + Sum('material_cost') + Sum('additional_costs')
    )
    
    # Worker stats
    total_workers = Worker.objects.count()
    available_workers = Worker.objects.filter(is_available=True).count()
    
    return Response({
        'customers': {
            'total': total_customers
        },
        'jobs': {
            'total': total_jobs,
            'active': active_jobs,
            'scheduled': scheduled_jobs,
            'completed': completed_jobs
        },
        'estimates': {
            'pending': pending_estimates,
            'accepted': accepted_estimates
        },
        'invoices': {
            'total': total_invoices,
            'paid': paid_invoices,
            'overdue': overdue_invoices
        },
        'revenue': {
            'total': float(total_revenue),
            'pending': 0  # This would need more complex calculation
        },
        'workers': {
            'total': total_workers,
            'available': available_workers
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_charts(request):
    """
    Generate dashboard charts using matplotlib
    Returns base64 encoded images
    """
    charts = {}
    
    # 1. Job Status Distribution
    job_status_data = Job.objects.values('status').annotate(count=Count('id'))
    if job_status_data:
        fig, ax = plt.subplots(figsize=(8, 6))
        statuses = [item['status'] for item in job_status_data]
        counts = [item['count'] for item in job_status_data]
        ax.pie(counts, labels=statuses, autopct='%1.1f%%', startangle=90)
        ax.set_title('Job Status Distribution')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        charts['job_status'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()
    
    # 2. Revenue Over Time (Last 6 months)
    six_months_ago = timezone.now().date() - timedelta(days=180)
    invoices = Invoice.objects.filter(
        invoice_date__gte=six_months_ago
    ).order_by('invoice_date')
    
    if invoices.exists():
        fig, ax = plt.subplots(figsize=(10, 6))
        dates = [inv.invoice_date for inv in invoices]
        amounts = [float(inv.total_amount) for inv in invoices]
        
        ax.plot(dates, amounts, marker='o', linestyle='-', linewidth=2, markersize=6)
        ax.set_xlabel('Date')
        ax.set_ylabel('Amount ($)')
        ax.set_title('Revenue Over Time (Last 6 Months)')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        charts['revenue_trend'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()
    
    # 3. Worker Type Distribution
    worker_data = Worker.objects.values('worker_type').annotate(count=Count('id'))
    if worker_data:
        fig, ax = plt.subplots(figsize=(10, 6))
        worker_types = [Worker.WORKER_TYPES[item['worker_type']][1] if any(wt[0] == item['worker_type'] for wt in Worker.WORKER_TYPES) else item['worker_type'] for item in worker_data]
        counts = [item['count'] for item in worker_data]
        
        ax.bar(worker_types, counts, color='skyblue')
        ax.set_xlabel('Worker Type')
        ax.set_ylabel('Count')
        ax.set_title('Worker Type Distribution')
        plt.xticks(rotation=45, ha='right')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        charts['worker_distribution'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()
    
    # 4. Invoice Status Distribution
    invoice_status_data = Invoice.objects.values('status').annotate(count=Count('id'))
    if invoice_status_data:
        fig, ax = plt.subplots(figsize=(8, 6))
        statuses = [item['status'] for item in invoice_status_data]
        counts = [item['count'] for item in invoice_status_data]
        
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff6666']
        ax.bar(statuses, counts, color=colors[:len(statuses)])
        ax.set_xlabel('Status')
        ax.set_ylabel('Count')
        ax.set_title('Invoice Status Distribution')
        plt.xticks(rotation=45)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        charts['invoice_status'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()
    
    # 5. Monthly Job Completion Rate (Last 12 months)
    one_year_ago = timezone.now().date() - timedelta(days=365)
    completed_jobs = Job.objects.filter(
        actual_end_date__gte=one_year_ago,
        status='COMPLETED'
    )
    
    if completed_jobs.exists():
        # Group by month
        from collections import defaultdict
        monthly_data = defaultdict(int)
        for job in completed_jobs:
            month_key = job.actual_end_date.strftime('%Y-%m')
            monthly_data[month_key] += 1
        
        if monthly_data:
            fig, ax = plt.subplots(figsize=(12, 6))
            months = sorted(monthly_data.keys())
            counts = [monthly_data[month] for month in months]
            
            ax.plot(months, counts, marker='o', linestyle='-', linewidth=2, markersize=8, color='green')
            ax.set_xlabel('Month')
            ax.set_ylabel('Jobs Completed')
            ax.set_title('Monthly Job Completion Rate')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            charts['monthly_completions'] = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()
            plt.close()
    
    return Response(charts)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reports(request):
    """
    Generate various reports for the system
    """
    report_type = request.query_params.get('type', 'summary')
    
    if report_type == 'summary':
        # Overall system summary
        return Response({
            'total_customers': Customer.objects.count(),
            'total_jobs': Job.objects.count(),
            'total_revenue': float(Invoice.objects.filter(status='PAID').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0),
            'active_jobs': Job.objects.filter(status='IN_PROGRESS').count(),
            'pending_invoices': Invoice.objects.filter(status__in=['SENT', 'OVERDUE']).count(),
        })
    
    elif report_type == 'customer':
        # Customer report with their jobs and payments
        customers = Customer.objects.all()
        customer_data = []
        for customer in customers:
            customer_data.append({
                'id': customer.id,
                'name': customer.full_name,
                'email': customer.email,
                'total_jobs': customer.jobs.count(),
                'completed_jobs': customer.jobs.filter(status='COMPLETED').count(),
                'total_spent': float(customer.invoices.filter(status='PAID').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0)
            })
        return Response(customer_data)
    
    elif report_type == 'financial':
        # Financial report
        paid_invoices = Invoice.objects.filter(status='PAID')
        unpaid_invoices = Invoice.objects.filter(status__in=['SENT', 'OVERDUE'])
        
        return Response({
            'total_revenue': float(paid_invoices.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0),
            'pending_revenue': float(unpaid_invoices.count()) * 1000,  # Simplified
            'total_invoices': Invoice.objects.count(),
            'paid_invoices': paid_invoices.count(),
            'unpaid_invoices': unpaid_invoices.count(),
        })
    
    return Response({'error': 'Invalid report type'}, status=status.HTTP_400_BAD_REQUEST)
