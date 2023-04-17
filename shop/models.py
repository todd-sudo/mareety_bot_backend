import datetime

from django.db import models


class Category(models.Model):

    name = models.CharField("Имя категории", max_length=255)
    slug = models.SlugField("Slug", unique=True)
    url = models.CharField("URL", max_length=800)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = "categories"


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name="products"
    )
    title = models.CharField("Наименование", max_length=500)
    url = models.CharField("URL", max_length=500)
    slug = models.SlugField("Slug", unique=True)
    image = models.CharField("Изображение", null=True, blank=True, max_length=1000)
    description = models.TextField("Описание", null=True, blank=True)
    price = models.DecimalField("Цена", max_digits=9, decimal_places=2)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        db_table = "products"


class CartProduct(models.Model):

    customer = models.ForeignKey(
        'Customer',
        verbose_name='Покупатель',
        on_delete=models.CASCADE,
        related_name="cart_products"
    )
    cart = models.ForeignKey(
        'Cart',
        verbose_name='Корзина',
        on_delete=models.CASCADE,
        related_name='cart_products'
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.CASCADE,
        related_name="cart_products"
    )
    qty = models.PositiveIntegerField("Кол-во", default=1)
    final_price = models.DecimalField(
        'Общая цена', max_digits=9, decimal_places=2
    )

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
        db_table = "cart_products"


class Cart(models.Model):
    """" Корзина
    """
    customer = models.ForeignKey(
        'Customer',
        null=True,
        verbose_name='Владелец',
        on_delete=models.CASCADE,
        related_name="carts"
    )
    products = models.ManyToManyField(
        CartProduct, blank=True, related_name='carts', verbose_name="Товары"
    )
    total_products = models.PositiveIntegerField("Всего товаров", default=0)
    final_price = models.DecimalField(
        'Общая цена', max_digits=9, default=0, decimal_places=2
    )
    is_order = models.BooleanField("В заказе", default=False)

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        db_table = "carts"


class Customer(models.Model):
    LangChoices = (
        ("en", 'en'),
        ("ru", 'ru'),
        ("uz", 'uz'),
    )

    tg_user_id = models.CharField("Телеграм ID", max_length=50)
    first_name = models.CharField("Имя", max_length=300)
    last_name = models.CharField("Фамилия", max_length=300)
    phone = models.CharField(
        max_length=20,
        verbose_name='Номер телефона',
        null=True,
        blank=True,
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Адрес',
        null=True,
        blank=True
    )
    create_at = models.DateField(
        "Дата создания", default=datetime.date.today()
    )
    lang = models.CharField(
        "Язык", default="uz", max_length=5, choices=LangChoices
    )

    def __str__(self):
        return "Покупатель: {} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"
        db_table = "customers"


class Order(models.Model):
    """Заказ товара пользователем"""
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(
        Customer,
        verbose_name='Покупатель',
        related_name='orders',
        on_delete=models.CASCADE
    )
    cart = models.ForeignKey(
        Cart,
        verbose_name='Корзина',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="orders"
    )
    address = models.CharField(
        'Адрес',
        max_length=1024,
        null=True,
        blank=True
    )
    status = models.CharField(
        'Статус заказ',
        max_length=100,
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    created_at = models.DateField("Дата создания заказа")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        db_table = "orders"

