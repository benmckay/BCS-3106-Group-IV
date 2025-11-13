from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    CustomerViewSet, WorkerViewSet, EstimateViewSet,
    JobViewSet, SupplierViewSet, MaterialViewSet,
    InvoiceViewSet, PaymentViewSet,
    register_user, current_user,
    dashboard_stats, dashboard_charts, reports
)

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'workers', WorkerViewSet, basename='worker')
router.register(r'estimates', EstimateViewSet, basename='estimate')
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', register_user, name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user/', current_user, name='current_user'),
    
    # Dashboard endpoints
    path('dashboard/stats/', dashboard_stats, name='dashboard_stats'),
    path('dashboard/charts/', dashboard_charts, name='dashboard_charts'),
    path('reports/', reports, name='reports'),
    
    # Include router URLs
    path('', include(router.urls)),
]

