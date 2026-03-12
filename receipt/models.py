from django.db import models
from catalog.models import Product
from account.models import User


class Receipt(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('confirmed', 'Проведён'),
    ]
    number = models.CharField('Номер чека', max_length=50, unique=True)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='receipts')
    created_at = models.DateTimeField('Дата', auto_now_add=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='draft')
    total = models.DecimalField('Итого', max_digits=14, decimal_places=2, default=0)
    note = models.TextField('Примечание', blank=True)

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'
        ordering = ['-created_at']

    def __str__(self):
        return f'Чек №{self.number}'

    def calc_total(self):
        self.total = sum(item.subtotal for item in self.items.all())
        self.save()


class ReceiptItem(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField('Название товара', max_length=255)
    price = models.DecimalField('Цена', max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)
    subtotal = models.DecimalField('Сумма', max_digits=14, decimal_places=2)

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'

    def save(self, *args, **kwargs):
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)


class Supply(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидается'),
        ('received', 'Получено'),
    ]
    number = models.CharField('Номер поставки', max_length=50, unique=True)
    supplier = models.CharField('Поставщик', max_length=255)
    created_at = models.DateTimeField('Дата', auto_now_add=True)
    received_at = models.DateTimeField('Получено', null=True, blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField('Итого', max_digits=14, decimal_places=2, default=0)
    note = models.TextField('Примечание', blank=True)

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'
        ordering = ['-created_at']

    def __str__(self):
        return f'Поставка №{self.number}'


class SupplyItem(models.Model):
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField('Название товара', max_length=255)
    cost_price = models.DecimalField('Цена закупки', max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)
    subtotal = models.DecimalField('Сумма', max_digits=14, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cost_price * self.quantity
        super().save(*args, **kwargs)
