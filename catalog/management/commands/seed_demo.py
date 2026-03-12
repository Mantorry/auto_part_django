"""
Команда для заполнения демо-данными:
- 3 пользователя (продавец, сортировщик, администратор)
- 30 товаров с реалистичными данными
- 50 чеков за последние 2 месяца
- 10 поставок за последние 2 месяца
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
import decimal


class Command(BaseCommand):
    help = 'Заполнить базу демо-данными'

    def handle(self, *args, **options):
        self._create_users()
        self._create_products()
        self._create_receipts_and_supplies()
        self.stdout.write(self.style.SUCCESS('✓ Демо-данные успешно загружены!'))

    # ------------------------------------------------------------------
    def _create_users(self):
        from account.models import User
        users_data = [
            {
                'full_name': 'Петров Алексей Дмитриевич',
                'username': 'petrov',
                'password': 'seller123',
                'role': 'seller',
            },
            {
                'full_name': 'Сидорова Марина Викторовна',
                'username': 'sidorova',
                'password': 'sorter123',
                'role': 'sorter',
            },
            {
                'full_name': 'Козлов Иван Сергеевич',
                'username': 'kozlov',
                'password': 'admin123',
                'role': 'admin',
                'is_superuser': True,
            },
        ]
        for data in users_data:
            if not User.objects.filter(username=data['username']).exists():
                u = User(
                    full_name=data['full_name'],
                    username=data['username'],
                    role=data['role'],
                    is_superuser=data.get('is_superuser', False),
                    is_active=True,
                )
                u.set_password(data['password'])
                u.save()
                self.stdout.write(f'  Пользователь: {data["full_name"]} ({data["role"]})')

    # ------------------------------------------------------------------
    def _create_products(self):
        from catalog.models import Category, Subcategory, Product

        products_data = [
            # BMW M3
            {
                'name': 'Тормозные колодки передние BMW M3 E46',
                'description': 'Высокопроизводительные тормозные колодки для BMW M3 E46. Обеспечивают отличную остановку при высоких нагрузках. Совместимы с оригинальными суппортами Brembo.',
                'cat': 'BMW', 'sub': 'M3',
                'price': 4800, 'stock': 12, 'sold': 34,
                'image_hint': 'brake-pads-bmw.jpg',
            },
            {
                'name': 'Амортизатор передний BMW M3 F80',
                'description': 'Газонаполненный амортизатор передней подвески BMW M3 F80. Производитель Bilstein. Восстанавливает заводскую жёсткость подвески, устраняет крены в поворотах.',
                'cat': 'BMW', 'sub': 'M3',
                'price': 14200, 'stock': 5, 'sold': 18,
            },
            # BMW M5
            {
                'name': 'Масляный фильтр BMW M5 F90',
                'description': 'Оригинальный масляный фильтр для BMW M5 F90 (S63 4.4L V8 Biturbo). Артикул 11427848321. Обеспечивает полную фильтрацию масла двигателя.',
                'cat': 'BMW', 'sub': 'M5',
                'price': 890, 'stock': 28, 'sold': 67, 'discount': 5,
            },
            {
                'name': 'Ремень ГРМ комплект BMW M5 E39',
                'description': 'Комплект замены ремня ГРМ для BMW M5 E39 (S62 V8). В комплект входят ремень, натяжной ролик, помпа охлаждения. Производитель Gates.',
                'cat': 'BMW', 'sub': 'M5',
                'price': 7600, 'stock': 3, 'sold': 11,
            },
            # BMW X5
            {
                'name': 'Воздушный фильтр BMW X5 E70 3.0d',
                'description': 'Фильтр воздушный для BMW X5 E70 с двигателем 3.0d (N57). Производитель Mann-Filter. Улучшает тягу и снижает расход топлива.',
                'cat': 'BMW', 'sub': 'X5',
                'price': 1350, 'stock': 18, 'sold': 44,
            },
            {
                'name': 'Рулевая рейка BMW X5 F15',
                'description': 'Рулевая рейка с электроусилителем для BMW X5 F15. Контрактная деталь в отличном состоянии. Пробег до 60 000 км. Гарантия 3 месяца.',
                'cat': 'BMW', 'sub': 'X5',
                'price': 42000, 'stock': 2, 'sold': 4,
            },
            # Mercedes C-Class
            {
                'name': 'Свечи зажигания Mercedes C200 W205',
                'description': 'Комплект 4 шт. свечей зажигания NGK для Mercedes-Benz C200 W205 (M274 2.0T). Иридиевые электроды для длительного срока службы.',
                'cat': 'Mercedes-Benz', 'sub': 'C-Class',
                'price': 3200, 'stock': 22, 'sold': 55, 'discount': 10,
            },
            {
                'name': 'Задние тормозные диски Mercedes C63 AMG W205',
                'description': 'Вентилируемые перфорированные тормозные диски задние для Mercedes C63 AMG W205. Производитель Brembo. Диаметр 330 мм.',
                'cat': 'Mercedes-Benz', 'sub': 'C-Class',
                'price': 18500, 'stock': 4, 'sold': 9,
            },
            # Mercedes E-Class
            {
                'name': 'Генератор Mercedes E300 W213',
                'description': 'Генератор Bosch 14V 180A для Mercedes E300 W213 (M264). Восстановленный, проверен на стенде. Аналог оригинала A0009064112.',
                'cat': 'Mercedes-Benz', 'sub': 'E-Class',
                'price': 22000, 'stock': 3, 'sold': 7,
            },
            {
                'name': 'Фильтр топливный Mercedes E220d W213',
                'description': 'Топливный фильтр Mann-Filter для Mercedes E220d W213 (OM 654). Очищает дизельное топливо от примесей, продлевает ресурс ТНВД.',
                'cat': 'Mercedes-Benz', 'sub': 'E-Class',
                'price': 2100, 'stock': 14, 'sold': 31,
            },
            # Audi A4
            {
                'name': 'Сцепление комплект Audi A4 B8 2.0 TDI',
                'description': 'Полный комплект сцепления LuK для Audi A4 B8 2.0 TDI (CAGA). Диск, корзина, выжимной подшипник. Момент затяжки 160 Нм.',
                'cat': 'Audi', 'sub': 'A4',
                'price': 16800, 'stock': 6, 'sold': 15,
            },
            {
                'name': 'Стойка стабилизатора передняя Audi A4 B9',
                'description': 'Стойка стабилизатора передней подвески для Audi A4 B9. Производитель Lemförder. Оригинальный артикул 8W0411317D.',
                'cat': 'Audi', 'sub': 'A4',
                'price': 1900, 'stock': 16, 'sold': 38, 'discount': 8,
            },
            # Audi Q5
            {
                'name': 'АКПП Audi Q5 8R 2.0 TFSI S-tronic',
                'description': 'Автоматическая коробка передач DL501 (7-ступенчатый S-tronic) для Audi Q5 8R 2.0 TFSI. Контрактная, из Германии. Пробег ~90 000 км.',
                'cat': 'Audi', 'sub': 'Q5',
                'price': 95000, 'stock': 1, 'sold': 2,
            },
            {
                'name': 'Форсунка инжектора Audi Q5 3.0 TDI',
                'description': 'Пьезофорсунка Bosch 0445116030 для Audi Q5 3.0 TDI (CDUC). Восстановленная, прошла полный цикл проверки на стенде.',
                'cat': 'Audi', 'sub': 'Q5',
                'price': 26000, 'stock': 4, 'sold': 8,
            },
            # VW Golf
            {
                'name': 'Стартер VW Golf VII 1.4 TSI',
                'description': 'Стартер Bosch 12V 1.1 кВт для Volkswagen Golf VII 1.4 TSI (CZEA). Восстановленный, гарантия 6 месяцев. Артикул 02Z911023E.',
                'cat': 'Volkswagen', 'sub': 'Golf',
                'price': 9800, 'stock': 5, 'sold': 13,
            },
            {
                'name': 'Ступичный подшипник VW Golf VI задний',
                'description': 'Ступичный подшипник FAG задней оси для VW Golf VI. Устанавливается в сборе со ступицей. Размер: 72×25×42.',
                'cat': 'Volkswagen', 'sub': 'Golf',
                'price': 3400, 'stock': 11, 'sold': 29, 'discount': 7,
            },
            # VW Passat
            {
                'name': 'EGR клапан VW Passat B8 2.0 TDI',
                'description': 'Клапан рециркуляции отработавших газов (EGR) для Volkswagen Passat B8 2.0 TDI (DFHA). Производитель Pierburg.',
                'cat': 'Volkswagen', 'sub': 'Passat',
                'price': 8700, 'stock': 7, 'sold': 16,
            },
            # Toyota Camry
            {
                'name': 'ШРУС наружный Toyota Camry V70 2.5',
                'description': 'ШРУС (граната) наружный левый / правый для Toyota Camry XV70 2.5 (A25A-FKS). Производитель NTN. В комплекте пыльник и хомуты.',
                'cat': 'Toyota', 'sub': 'Camry',
                'price': 6200, 'stock': 9, 'sold': 22, 'discount': 12,
            },
            {
                'name': 'Термостат Toyota Camry V50 2.5',
                'description': 'Термостат охлаждающей жидкости для Toyota Camry V50 2.5 (2AR-FE). Производитель Gates. Температура открытия 82°C.',
                'cat': 'Toyota', 'sub': 'Camry',
                'price': 2400, 'stock': 13, 'sold': 35,
            },
            # Toyota Land Cruiser
            {
                'name': 'Передний бампер Toyota Land Cruiser 200',
                'description': 'Бампер передний в сборе для Toyota Land Cruiser 200 (рестайлинг 2015-2021). Цвет: белый перламутр (070). Оригинал.',
                'cat': 'Toyota', 'sub': 'Land Cruiser',
                'price': 67000, 'stock': 2, 'sold': 3,
            },
            # Honda Civic
            {
                'name': 'Катализатор Honda Civic X 1.5T',
                'description': 'Каталитический нейтрализатор для Honda Civic X 1.5T (L15B7). Металлический носитель высокой плотности, соответствует нормам Евро-6.',
                'cat': 'Honda', 'sub': 'Civic',
                'price': 34000, 'stock': 3, 'sold': 6,
            },
            {
                'name': 'Тросик ручного тормоза Honda Civic IX задний',
                'description': 'Трос ручного тормоза задний для Honda Civic IX (FB). Производитель Cofle. Длина 1840 мм.',
                'cat': 'Honda', 'sub': 'Civic',
                'price': 1600, 'stock': 20, 'sold': 42, 'discount': 5,
            },
            # Ford Focus
            {
                'name': 'Рычаг подвески Ford Focus III передний левый',
                'description': 'Поперечный рычаг передней подвески левый для Ford Focus III (CB8). Производитель Lemförder. Идёт в сборе с шаровой опорой.',
                'cat': 'Ford', 'sub': 'Focus',
                'price': 5400, 'stock': 8, 'sold': 19,
            },
            {
                'name': 'Радиатор охлаждения Ford Focus II 1.8',
                'description': 'Радиатор охлаждения двигателя Ford Focus II 1.8 (QQDB). Производитель NISSENS. Размер 650×378 мм, алюминий + пластик.',
                'cat': 'Ford', 'sub': 'Focus',
                'price': 7900, 'stock': 5, 'sold': 12,
            },
            # Nissan Qashqai
            {
                'name': 'Датчик кислорода Nissan Qashqai J11 2.0',
                'description': 'Лямбда-зонд верхний (до катализатора) для Nissan Qashqai J11 2.0 (MR20DD). Производитель Denso. Подходит для J11, J11R.',
                'cat': 'Nissan', 'sub': 'Qashqai',
                'price': 4100, 'stock': 10, 'sold': 27, 'discount': 15,
            },
            {
                'name': 'Комплект поршневых колец Nissan X-Trail T32 2.5',
                'description': 'Поршневые кольца (комплект на 4 цилиндра) для Nissan X-Trail T32 2.5 (QR25DE). Производитель NPR Japan. Размер: STD.',
                'cat': 'Nissan', 'sub': 'X-Trail',
                'price': 8200, 'stock': 6, 'sold': 10,
            },
            # Hyundai Tucson
            {
                'name': 'Насос гидроусилителя Hyundai Tucson TL 2.0',
                'description': 'Насос гидроусилителя руля для Hyundai Tucson TL 2.0 (G4NA). Производитель Mando. Давление: 120 бар. Новый.',
                'cat': 'Hyundai', 'sub': 'Tucson',
                'price': 18900, 'stock': 4, 'sold': 7,
            },
            {
                'name': 'Задний сайлентблок Hyundai Elantra AD рычага',
                'description': 'Сайлентблок заднего поперечного рычага для Hyundai Elantra AD. Производитель CTR. Гарантия 2 года / 50 000 км.',
                'cat': 'Hyundai', 'sub': 'Elantra',
                'price': 1200, 'stock': 25, 'sold': 58, 'discount': 5,
            },
            # Kia Sportage
            {
                'name': 'Комплект ГРМ Kia Sportage IV 2.0',
                'description': 'Комплект цепи ГРМ для Kia Sportage QL 2.0 (G4NA). В комплект входят: цепь ГРМ, успокоитель, натяжитель, звёздочка. Производитель Iwis.',
                'cat': 'Kia', 'sub': 'Sportage',
                'price': 11500, 'stock': 7, 'sold': 17,
            },
            {
                'name': 'Стекло лобовое Kia Sorento II XM',
                'description': 'Лобовое стекло для Kia Sorento II XM (2009-2012). Производитель AGC Japan. С местом под зеркало. Тепловая полоса, датчик дождя.',
                'cat': 'Kia', 'sub': 'Sorento',
                'price': 21000, 'stock': 3, 'sold': 5,
            },
            # Общее — Тормозная система
            {
                'name': 'Тормозная жидкость DOT 4 1L универсальная',
                'description': 'Тормозная жидкость DOT4 объём 1 литр. Производитель ATE. Температура кипения: 230°C (сухая) / 155°C (мокрая). Совместима со всеми марками.',
                'cat': 'Запчасти (общее)', 'sub': 'Тормозная система',
                'price': 780, 'stock': 35, 'sold': 94, 'discount': 0,
            },
            {
                'name': 'Аккумулятор автомобильный 60Ah 600A',
                'description': 'Аккумулятор VARTA Blue Dynamic 60Ah 600A (EN). Тип клемм: стандартные. Полярность: обратная. Подходит для большинства автомобилей объёмом 1.4–2.0L.',
                'cat': 'Запчасти (общее)', 'sub': 'Электрика',
                'price': 8500, 'stock': 8, 'sold': 23, 'discount': 0,
            },
        ]

        from catalog.models import Category, Subcategory, Product
        created = 0
        for pd in products_data:
            if Product.objects.filter(name=pd['name']).exists():
                continue
            cat = Category.objects.filter(name=pd['cat']).first()
            sub = None
            if cat and pd.get('sub'):
                sub = Subcategory.objects.filter(category=cat, name=pd['sub']).first()
            p = Product.objects.create(
                name=pd['name'],
                description=pd['description'],
                category=cat,
                subcategory=sub,
                price=pd['price'],
                stock=pd['stock'],
                sold_count=pd.get('sold', 0),
                discount=pd.get('discount', 0),
                is_active=True,
            )
            created += 1
        self.stdout.write(f'  Товаров создано: {created}')

    # ------------------------------------------------------------------
    def _create_receipts_and_supplies(self):
        from account.models import User
        from catalog.models import Product
        from receipt.models import Receipt, ReceiptItem, Supply, SupplyItem
        import uuid

        sellers = list(User.objects.filter(role='seller'))
        if not sellers:
            sellers = list(User.objects.all()[:1])
        products = list(Product.objects.filter(is_active=True))
        if not products:
            self.stdout.write(self.style.WARNING('  Товары не найдены, пропускаю чеки'))
            return

        now = timezone.now()
        two_months_ago = now - timedelta(days=62)

        # --- Receipts: 52 шт ---
        receipt_count = 0
        for i in range(52):
            days_back = random.randint(0, 61)
            dt = now - timedelta(days=days_back, hours=random.randint(0, 10), minutes=random.randint(0, 59))
            seller = random.choice(sellers)
            num = f'CHK-{dt.strftime("%Y%m%d")}-{str(uuid.uuid4())[:4].upper()}'
            if Receipt.objects.filter(number=num).exists():
                continue
            receipt = Receipt.objects.create(
                number=num,
                seller=seller,
                status='confirmed',
                total=0,
                created_at=dt,
            )
            # Обход auto_now_add через update
            Receipt.objects.filter(pk=receipt.pk).update(created_at=dt)

            n_items = random.randint(1, 4)
            chosen = random.sample(products, min(n_items, len(products)))
            total = decimal.Decimal('0')
            for prod in chosen:
                qty = random.randint(1, 3)
                price = prod.final_price
                subtotal = price * qty
                total += subtotal
                ReceiptItem.objects.create(
                    receipt=receipt,
                    product=prod,
                    product_name=prod.name,
                    price=price,
                    quantity=qty,
                    subtotal=subtotal,
                )
            Receipt.objects.filter(pk=receipt.pk).update(total=total)
            receipt_count += 1
        self.stdout.write(f'  Чеков создано: {receipt_count}')

        # --- Supplies: 10 шт ---
        suppliers = [
            'ООО «АвтоДеталь Опт»',
            'АО «Запчасти Плюс»',
            'ИП Волков А.В.',
            'ООО «МоторМаркет»',
            'GmbH AutoTeile DE',
        ]
        supply_count = 0
        for i in range(10):
            days_back = random.randint(5, 62)
            dt = now - timedelta(days=days_back)
            supplier = random.choice(suppliers)
            num = f'SUP-{dt.strftime("%Y%m%d")}-{str(uuid.uuid4())[:4].upper()}'
            if Supply.objects.filter(number=num).exists():
                continue
            status = 'received' if days_back > 7 else 'pending'
            supply = Supply.objects.create(
                number=num,
                supplier=supplier,
                status=status,
                total=0,
                created_at=dt,
            )
            Supply.objects.filter(pk=supply.pk).update(created_at=dt)

            n_items = random.randint(3, 7)
            chosen = random.sample(products, min(n_items, len(products)))
            total = decimal.Decimal('0')
            for prod in chosen:
                qty = random.randint(5, 20)
                cost = prod.price * decimal.Decimal('0.65')
                subtotal = cost * qty
                total += subtotal
                SupplyItem.objects.create(
                    supply=supply,
                    product=prod,
                    product_name=prod.name,
                    cost_price=round(cost, 2),
                    quantity=qty,
                    subtotal=round(subtotal, 2),
                )
            Supply.objects.filter(pk=supply.pk).update(total=round(total, 2))
            supply_count += 1
        self.stdout.write(f'  Поставок создано: {supply_count}')
