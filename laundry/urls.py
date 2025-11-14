from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    home,
    AuthLoginView,
    dashboard,
    employee_dashboard,
    owner_dashboard,
    order_create,
    order_detail,
    check_status,
    customers_list,
    employees_list,
    transactions_list,
    update_status,
    monthly_report,
    add_customer_api,
)


urlpatterns = [
    path('', home, name='home'),
    path('login/', AuthLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/pegawai/', employee_dashboard, name='employee_dashboard'),
    path('dashboard/owner/', owner_dashboard, name='owner_dashboard'),
    path('order/new/', order_create, name='order_create'),
    path('order/<str:order_number>/', order_detail, name='order_detail'),
    path('status/', check_status, name='check_status'),
    path('pelanggan/', customers_list, name='customers_list'),
    path('pegawai/', employees_list, name='employees_list'),
    path('transaksi/', transactions_list, name='transactions_list'),
    path('transaksi/<int:pk>/status/', update_status, name='update_status'),
    path('laporan-bulanan/', monthly_report, name='monthly_report'),
    path('api/add-customer/', add_customer_api, name='add_customer_api'),
]