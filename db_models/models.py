from django.db import models
from django.contrib.auth.models import User
from .help import SaveMediaFile, PriceType


class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id', ]
        indexes = [models.Index(fields=['id'])]
        verbose_name = 'status'


class OurTeam(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=SaveMediaFile.employee)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id', ]
        indexes = [models.Index(fields=['id'])]
        verbose_name = 'our_team'


class Comments(models.Model):
    text = models.TextField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:10]

    class Meta:
        ordering = ['id', ]
        indexes = [models.Index(fields=['id'])]
        verbose_name = 'comments'


class Category(models.Model):
    title = models.CharField(max_length=50)
    products_count = models.IntegerField(default=0)
    photo = models.ImageField(upload_to=SaveMediaFile.category)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id', ]
        indexes = [models.Index(fields=['id'])]
        verbose_name = 'category'


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    manufacturer_name = models.CharField(max_length=100)
    discount = models.FloatField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=SaveMediaFile.product)
    popular_products = models.IntegerField(default=0)
    price = models.FloatField()
    price_type = models.CharField(max_length=10, choices=PriceType.choices, default=PriceType.USD)
    rating = models.FloatField(default=0)
    comments = models.ManyToManyField(Comments, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id', ]
        indexes = [models.Index(fields=['id'])]
        verbose_name = 'products'


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_number = models.IntegerField(default=1)
    payment_status = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)
    price_type = models.CharField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.price_type

    class Meta:
        ordering = ['id', ]
        indexes = [models.Index(fields=['id'])]
        verbose_name = 'cart'


class ProductsUsers(models.Model):
    full_name = models.CharField(verbose_name='Full name', max_length=100, null=True)
    username = models.CharField(verbose_name='Username', max_length=20, unique=True, null=True)
    telegram_id = models.PositiveBigIntegerField(verbose_name='Telegram ID', unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products_users'


class ProductsProducts(models.Model):
    id = models.AutoField(primary_key=True)
    poroduct_name = models.CharField(verbose_name='Maxsulot nomi ', max_length=50)
    photo = models.CharField(verbose_name="Rasm file_id", max_length=200)
    price = models.DecimalField(verbose_name='Narx', decimal_places=2, max_digits=10)
    description = models.TextField(verbose_name='Maxsulto xaqida', max_length=300)
    category_code = models.CharField(verbose_name='Category code', max_length=30)
    category_name = models.CharField(verbose_name='Kategoriya nomi', max_length=40)
    subcategory_code = models.CharField(verbose_name='Ost_categoriya kodi', max_length=50)
    subcategory_name = models.CharField(verbose_name='Ost-kategoriya nomi', max_length=50)

    def __str__(self):
        return f"{self.id}-{self.poroduct_name}"

    class Meta:
        db_table = 'products_product'
