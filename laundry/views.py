from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict
from .forms import LoginForm, CustomerForm, EmployeeForm, OrderForm
from .models import Order, Customer


def home(request):
    return render(request, 'base.html', {
        'page_title': 'Money Laundry',
        'home': True,
    })


class AuthLoginView(LoginView):
    form_class = LoginForm
    template_name = 'laundry/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Login berhasil.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Username atau password salah.')
        return super().form_invalid(form)


@login_required
def dashboard(request):
    if request.user.role == 'OWNER':
        return redirect('owner_dashboard')
    return redirect('employee_dashboard')


@login_required
def employee_dashboard(request):
    return render(request, 'laundry/employee_dashboard.html')


@login_required
def owner_dashboard(request):
    if request.user.role != 'OWNER':
        return HttpResponseForbidden()
    return render(request, 'laundry/owner_dashboard.html')


@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, 'Order berhasil disimpan.')
            return redirect('order_detail', order_number=order.order_number)
        messages.error(request, 'Gagal menyimpan data order. Silakan coba lagi.')
    else:
        form = OrderForm()
    q = request.GET.get('q')
    customers = Customer.objects.all()
    if q:
        customers = customers.filter(name__icontains=q)
    return render(request, 'laundry/order_form.html', {'form': form, 'customers': customers})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'laundry/order_detail.html', {'order': order})


def check_status(request):
    result = None
    error = None
    number = ''
    if request.method == 'POST':
        number = request.POST.get('order_number', '').strip()
        try:
            result = Order.objects.select_related('customer').get(order_number=number)
            messages.success(request, 'Data pesanan ditemukan.')
        except Order.DoesNotExist:
            error = 'Nomor order tidak ditemukan.'
            messages.error(request, error)
    return render(request, 'laundry/check_status.html', {'result': result, 'order_number': number})


@login_required
def customers_list(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data pelanggan berhasil disimpan.')
            return redirect('customers_list')
        messages.error(request, 'Lengkapi semua data sebelum menyimpan.')
    else:
        form = CustomerForm()
    customers = Customer.objects.all()
    return render(request, 'laundry/customers.html', {'customers': customers, 'form': form})


@login_required
def employees_list(request):
    if request.user.role != 'OWNER':
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data pegawai berhasil disimpan.')
            return redirect('employees_list')
        messages.error(request, 'Lengkapi semua data sebelum menyimpan.')
    else:
        form = EmployeeForm()
    return render(request, 'laundry/employees.html', {'form': form})


@login_required
def transactions_list(request):
    orders = Order.objects.select_related('customer').all().order_by('-updated_at')
    return render(request, 'laundry/transactions.html', {'orders': orders})


@login_required
def update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            messages.success(request, 'Status berhasil diperbarui.')
        else:
            messages.error(request, 'Gagal memperbarui status. Silakan coba lagi.')
    return redirect('transactions_list')


@login_required
def monthly_report(request):
    if request.user.role != 'OWNER':
        return HttpResponseForbidden()
    
    # Get current month and year
    now = timezone.now()
    current_month = now.month
    current_year = now.year
    
    # Get month and year from request, default to current
    month = int(request.GET.get('month', current_month))
    year = int(request.GET.get('year', current_year))
    
    # Calculate date range for the selected month
    start_date = datetime(year, month, 1).date()
    if month == 12:
        end_date = datetime(year + 1, 1, 1).date() - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1).date() - timedelta(days=1)
    
    # Get orders for the selected month
    monthly_orders = Order.objects.filter(
        date_in__range=[start_date, end_date]
    ).select_related('customer')
    
    # Calculate statistics
    total_transactions = monthly_orders.count()
    total_revenue = monthly_orders.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    
    # Statistics by status
    status_stats = monthly_orders.values('status').annotate(
        count=Count('id'),
        revenue=Sum('total_cost')
    ).order_by('status')
    
    # Statistics by service type
    service_stats = monthly_orders.values('service_type').annotate(
        count=Count('id'),
        revenue=Sum('total_cost')
    ).order_by('service_type')
    
    # Daily statistics for the month
    daily_stats = []
    current_date = start_date
    while current_date <= end_date:
        day_orders = monthly_orders.filter(date_in=current_date)
        day_total = day_orders.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        day_count = day_orders.count()
        
        daily_stats.append({
            'date': current_date,
            'total_revenue': float(day_total),
            'transaction_count': day_count
        })
        current_date += timedelta(days=1)
    
    # Calculate monthly totals
    monthly_totals = {
        'total_transactions': total_transactions,
        'total_revenue': float(total_revenue),
        'average_per_transaction': float(total_revenue / total_transactions) if total_transactions > 0 else 0,
        'express_count': monthly_orders.filter(service_type='EXPRESS').count(),
        'regular_count': monthly_orders.filter(service_type='REGULAR').count(),
        'completed_count': monthly_orders.filter(status='SELESAI').count(),
        'in_progress_count': monthly_orders.filter(status='PROSES').count()
    }
    
    # Prepare data for charts
    chart_data = {
        'daily_labels': [stat['date'].strftime('%d') for stat in daily_stats],
        'daily_revenue': [stat['total_revenue'] for stat in daily_stats],
        'daily_transactions': [stat['transaction_count'] for stat in daily_stats],
        'status_labels': [stat['status'] for stat in status_stats],
        'status_counts': [stat['count'] for stat in status_stats],
        'service_labels': [stat['service_type'] for stat in service_stats],
        'service_revenue': [float(stat['revenue']) for stat in service_stats]
    }
    
    # Generate month choices for filter
    months = [
        {'value': i, 'name': datetime(2000, i, 1).strftime('%B'), 'selected': i == month}
        for i in range(1, 13)
    ]
    
    # Generate year choices (current year and previous 2 years)
    current_year = now.year
    years = [
        {'value': year, 'name': str(year), 'selected': year == current_year}
        for year in range(current_year - 2, current_year + 1)
    ]
    
    context = {
        'orders': monthly_orders,
        'monthly_totals': monthly_totals,
        'status_stats': status_stats,
        'service_stats': service_stats,
        'daily_stats': daily_stats,
        'chart_data': chart_data,
        'selected_month': month,
        'selected_year': year,
        'months': months,
        'years': years,
        'month_name': datetime(year, month, 1).strftime('%B %Y')
    }
    
    return render(request, 'laundry/monthly_report.html', context)


@login_required
def add_customer_api(request):
    """API endpoint untuk menambahkan pelanggan via AJAX"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        
        if not name or not phone:
            return JsonResponse({
                'success': False,
                'error': 'Nama dan nomor telepon wajib diisi.'
            })
        
        try:
            customer = Customer.objects.create(
                name=name,
                phone=phone,
                address=address
            )
            
            return JsonResponse({
                'success': True,
                'customer_id': customer.id,
                'customer_name': customer.name,
                'message': 'Pelanggan berhasil ditambahkan.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Method not allowed.'
    })