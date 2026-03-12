from django.shortcuts import render
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay, TruncMonth
from django.utils import timezone
from datetime import timedelta
from account.decorators import login_required_custom
from account.models import User
from catalog.models import Product
from receipt.models import Receipt, ReceiptItem
import json


@login_required_custom
def dashboard(request):
    user_id = request.session.get('user_id')
    notifications_enabled = True
    try:
        u = User.objects.get(id=user_id)
        notifications_enabled = u.notifications_enabled
    except:
        pass

    # Sales by day (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    sales_by_day = (
        Receipt.objects.filter(status='confirmed', created_at__gte=thirty_days_ago)
        .annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(total=Sum('total'), count=Count('id'))
        .order_by('day')
    )
    sales_labels = [s['day'].strftime('%d.%m') for s in sales_by_day]
    sales_data = [float(s['total']) for s in sales_by_day]

    # Monthly revenue
    now = timezone.now()
    month_revenue = Receipt.objects.filter(
        status='confirmed',
        created_at__year=now.year,
        created_at__month=now.month
    ).aggregate(total=Sum('total'))['total'] or 0

    year_revenue = Receipt.objects.filter(
        status='confirmed',
        created_at__year=now.year
    ).aggregate(total=Sum('total'))['total'] or 0

    # Monthly chart
    monthly = (
        Receipt.objects.filter(status='confirmed', created_at__year=now.year)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('total'))
        .order_by('month')
    )
    monthly_labels = [m['month'].strftime('%b') for m in monthly]
    monthly_data = [float(m['total']) for m in monthly]

    # Top 5 sold
    top_sold = (
        ReceiptItem.objects.filter(receipt__status='confirmed')
        .values('product_name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')[:5]
    )

    # Top 5 least sold
    least_sold = Product.objects.filter(is_active=True).order_by('sold_count')[:5]

    # Low stock notifications
    low_stock_products = Product.objects.filter(is_active=True, stock__lt=3) if notifications_enabled else []

    return render(request, 'dashboard/dashboard.html', {
        'sales_labels': json.dumps(sales_labels),
        'sales_data': json.dumps(sales_data),
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_data': json.dumps(monthly_data),
        'month_revenue': month_revenue,
        'year_revenue': year_revenue,
        'top_sold': top_sold,
        'least_sold': least_sold,
        'low_stock_products': low_stock_products,
        'notifications_enabled': notifications_enabled,
    })
