from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        db_table = 'subcategories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='product_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name

    @property
    def photo_url(self):
        if self.photo:
            return f"/media/{self.photo}"
        return ""


class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    is_subscribed = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username or f'User {self.telegram_id}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    class Meta:
        db_table = 'cart'

    def __str__(self):
        return f'{self.product_name} x{self.quantity}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    status = models.CharField(max_length=50, blank=True, null=True)
    delivery_info = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f'Order #{self.id} — {self.user}'


class BroadcastMessage(models.Model):
    text = models.TextField("Текст сообщения")
    image = models.ImageField("Картинка (опционально)", upload_to='broadcast_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Рассылка от {self.created_at:%Y-%m-%d %H:%M}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
