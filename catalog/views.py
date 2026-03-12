from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Category, Subcategory, Product
from account.decorators import login_required_custom
import json


@login_required_custom
def index(request):
    products = Product.objects.filter(is_active=True).select_related('category', 'subcategory')
    categories = Category.objects.prefetch_related('subcategories').all()

    q = request.GET.get('q', '')
    cat_ids = request.GET.getlist('category')
    sub_ids = request.GET.getlist('subcategory')
    sort = request.GET.get('sort', 'name')

    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if cat_ids:
        products = products.filter(category__id__in=cat_ids)
    if sub_ids:
        products = products.filter(subcategory__id__in=sub_ids)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('name')

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values()) if cart else 0

    return render(request, 'catalog/index.html', {
        'products': products,
        'categories': categories,
        'q': q,
        'cat_ids': [int(x) for x in cat_ids],
        'sub_ids': [int(x) for x in sub_ids],
        'sort': sort,
        'cart_count': cart_count,
    })


@login_required_custom
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, 'catalog/product_detail.html', {'product': product})


@login_required_custom
def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        try:
            p = Product.objects.get(id=int(pid))
            subtotal = p.final_price * qty
            total += subtotal
            items.append({'product': p, 'qty': qty, 'subtotal': subtotal})
        except Product.DoesNotExist:
            pass
    return render(request, 'catalog/cart.html', {'items': items, 'total': total})


@login_required_custom
def cart_add(request, pk):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        key = str(pk)
        qty = int(request.POST.get('qty', 1))
        cart[key] = cart.get(key, 0) + qty
        request.session['cart'] = cart
        request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', 'catalog:index'))


@login_required_custom
def cart_remove(request, pk):
    cart = request.session.get('cart', {})
    cart.pop(str(pk), None)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('catalog:cart')


@login_required_custom
def cart_update(request, pk):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        qty = int(request.POST.get('qty', 1))
        if qty > 0:
            cart[str(pk)] = qty
        else:
            cart.pop(str(pk), None)
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('catalog:cart')
