from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from account.decorators import login_required_custom, role_required
from account.models import User
from catalog.models import Category, Subcategory, Product
from receipt.models import Receipt, Supply
from django.contrib.auth.hashers import make_password


def admin_required(view_func):
    from functools import wraps
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('account:login')
        role = request.session.get('user_role')
        if role not in ('admin',) and not request.session.get('is_superuser'):
            try:
                u = User.objects.get(id=request.session['user_id'])
                if not (u.role == 'admin' or u.is_superuser):
                    return redirect('catalog:index')
            except:
                return redirect('catalog:index')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required_custom
@admin_required
def panel_index(request):
    return render(request, 'panel/index.html', {
        'user_count': User.objects.count(),
        'product_count': Product.objects.count(),
        'category_count': Category.objects.count(),
        'receipt_count': Receipt.objects.count(),
        'supply_count': Supply.objects.count(),
    })


# ---- USERS ----
@login_required_custom
@admin_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'panel/user_list.html', {'users': users})


@login_required_custom
@admin_required
def user_create(request):
    if request.method == 'POST':
        u = User(
            full_name=request.POST['full_name'],
            username=request.POST['username'],
            role=request.POST['role'],
        )
        u.set_password(request.POST['password'])
        u.save()
        messages.success(request, 'Пользователь создан')
        return redirect('panel:user_list')
    return render(request, 'panel/user_form.html', {'title': 'Новый пользователь'})


@login_required_custom
@admin_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.full_name = request.POST['full_name']
        user.username = request.POST['username']
        user.role = request.POST['role']
        user.is_active = request.POST.get('is_active') == 'on'
        if request.POST.get('password'):
            user.set_password(request.POST['password'])
        user.save()
        messages.success(request, 'Пользователь обновлён')
        return redirect('panel:user_list')
    return render(request, 'panel/user_form.html', {'title': 'Редактировать', 'obj': user})


@login_required_custom
@admin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Пользователь удалён')
        return redirect('panel:user_list')
    return render(request, 'panel/confirm_delete.html', {'obj': user, 'title': 'пользователя'})


# ---- CATEGORIES ----
@login_required_custom
@admin_required
def category_list(request):
    cats = Category.objects.prefetch_related('subcategories').all()
    return render(request, 'panel/category_list.html', {'categories': cats})


@login_required_custom
@admin_required
def category_create(request):
    if request.method == 'POST':
        Category.objects.create(name=request.POST['name'], slug=request.POST['slug'])
        messages.success(request, 'Категория создана')
        return redirect('panel:category_list')
    return render(request, 'panel/category_form.html', {'title': 'Новая категория'})


@login_required_custom
@admin_required
def category_edit(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        cat.name = request.POST['name']
        cat.slug = request.POST['slug']
        cat.save()
        messages.success(request, 'Категория обновлена')
        return redirect('panel:category_list')
    return render(request, 'panel/category_form.html', {'title': 'Редактировать', 'obj': cat})


@login_required_custom
@admin_required
def category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        cat.delete()
        return redirect('panel:category_list')
    return render(request, 'panel/confirm_delete.html', {'obj': cat, 'title': 'категорию'})


# ---- SUBCATEGORIES ----
@login_required_custom
@admin_required
def subcategory_list(request):
    subs = Subcategory.objects.select_related('category').all()
    return render(request, 'panel/subcategory_list.html', {'subcategories': subs})


@login_required_custom
@admin_required
def subcategory_create(request):
    cats = Category.objects.all()
    if request.method == 'POST':
        Subcategory.objects.create(
            category_id=request.POST['category'],
            name=request.POST['name'],
            slug=request.POST['slug'],
        )
        messages.success(request, 'Подкатегория создана')
        return redirect('panel:subcategory_list')
    return render(request, 'panel/subcategory_form.html', {'title': 'Новая подкатегория', 'categories': cats})


@login_required_custom
@admin_required
def subcategory_edit(request, pk):
    sub = get_object_or_404(Subcategory, pk=pk)
    cats = Category.objects.all()
    if request.method == 'POST':
        sub.category_id = request.POST['category']
        sub.name = request.POST['name']
        sub.slug = request.POST['slug']
        sub.save()
        messages.success(request, 'Подкатегория обновлена')
        return redirect('panel:subcategory_list')
    return render(request, 'panel/subcategory_form.html', {'title': 'Редактировать', 'obj': sub, 'categories': cats})


@login_required_custom
@admin_required
def subcategory_delete(request, pk):
    sub = get_object_or_404(Subcategory, pk=pk)
    if request.method == 'POST':
        sub.delete()
        return redirect('panel:subcategory_list')
    return render(request, 'panel/confirm_delete.html', {'obj': sub, 'title': 'подкатегорию'})


# ---- PRODUCTS ----
@login_required_custom
@admin_required
def product_list(request):
    products = Product.objects.select_related('category', 'subcategory').all()
    return render(request, 'panel/product_list.html', {'products': products})


@login_required_custom
@admin_required
def product_create(request):
    cats = Category.objects.prefetch_related('subcategories').all()
    if request.method == 'POST':
        p = Product(
            name=request.POST['name'],
            description=request.POST.get('description', ''),
            category_id=request.POST.get('category') or None,
            subcategory_id=request.POST.get('subcategory') or None,
            stock=request.POST.get('stock', 0),
            price=request.POST.get('price', 0),
            discount=request.POST.get('discount', 0),
            is_active=request.POST.get('is_active') == 'on',
        )
        if request.FILES.get('image'):
            p.image = request.FILES['image']
        p.save()
        messages.success(request, 'Товар создан')
        return redirect('panel:product_list')
    return render(request, 'panel/product_form.html', {'title': 'Новый товар', 'categories': cats})


@login_required_custom
@admin_required
def product_edit(request, pk):
    p = get_object_or_404(Product, pk=pk)
    cats = Category.objects.prefetch_related('subcategories').all()
    if request.method == 'POST':
        p.name = request.POST['name']
        p.description = request.POST.get('description', '')
        p.category_id = request.POST.get('category') or None
        p.subcategory_id = request.POST.get('subcategory') or None
        p.stock = request.POST.get('stock', 0)
        p.price = request.POST.get('price', 0)
        p.discount = request.POST.get('discount', 0)
        p.is_active = request.POST.get('is_active') == 'on'
        if request.FILES.get('image'):
            p.image = request.FILES['image']
        p.save()
        messages.success(request, 'Товар обновлён')
        return redirect('panel:product_list')
    return render(request, 'panel/product_form.html', {'title': 'Редактировать товар', 'obj': p, 'categories': cats})


@login_required_custom
@admin_required
def product_delete(request, pk):
    p = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        p.delete()
        return redirect('panel:product_list')
    return render(request, 'panel/confirm_delete.html', {'obj': p, 'title': 'товар'})


# ---- RECEIPTS (view only in panel) ----
@login_required_custom
@admin_required
def receipt_list(request):
    receipts = Receipt.objects.select_related('seller').all()
    return render(request, 'panel/receipt_list.html', {'receipts': receipts})


@login_required_custom
@admin_required
def receipt_delete(request, pk):
    r = get_object_or_404(Receipt, pk=pk)
    if request.method == 'POST':
        r.delete()
        return redirect('panel:receipt_list')
    return render(request, 'panel/confirm_delete.html', {'obj': r, 'title': 'чек'})


# ---- SUPPLIES ----
@login_required_custom
@admin_required
def supply_list(request):
    supplies = Supply.objects.all()
    return render(request, 'panel/supply_list.html', {'supplies': supplies})


@login_required_custom
@admin_required
def supply_create(request):
    products = Product.objects.filter(is_active=True)
    if request.method == 'POST':
        from receipt.models import SupplyItem
        import uuid
        from django.utils import timezone
        supply = Supply.objects.create(
            number=f'SUP-{timezone.now().strftime("%Y%m%d")}-{str(uuid.uuid4())[:4].upper()}',
            supplier=request.POST.get('supplier', ''),
            note=request.POST.get('note', ''),
        )
        total = 0
        pids = request.POST.getlist('product')
        qtys = request.POST.getlist('quantity')
        prices = request.POST.getlist('cost_price')
        for pid, qty, price in zip(pids, qtys, prices):
            if pid and qty and price:
                p = Product.objects.get(id=pid)
                item = SupplyItem.objects.create(
                    supply=supply,
                    product=p,
                    product_name=p.name,
                    cost_price=price,
                    quantity=qty,
                )
                total += item.subtotal
        supply.total = total
        supply.save()
        messages.success(request, 'Поставка создана')
        return redirect('panel:supply_list')
    return render(request, 'panel/supply_form.html', {'products': products})


@login_required_custom
@admin_required
def supply_delete(request, pk):
    s = get_object_or_404(Supply, pk=pk)
    if request.method == 'POST':
        s.delete()
        return redirect('panel:supply_list')
    return render(request, 'panel/confirm_delete.html', {'obj': s, 'title': 'поставку'})
