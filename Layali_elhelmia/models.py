from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import os 
from pgcrypto.fields import EncryptedCharField , EncryptedIntegerField , EncryptedEmailField
from django.utils import timezone
class Category(models.Model):
    name_in_english = models.CharField(max_length=35)
    name_in_arabic = models.CharField(max_length=35)
    image = models.ImageField(upload_to='images/category')

    def __str__(self):   
        return self.name_in_english + " | " + self.name_in_arabic
    def save(self, *args, **kwargs):
        try:
            this = Category.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
class Kind(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='kinds', null=True)
    name_in_english = models.CharField(max_length=35)
    name_in_arabic = models.CharField(max_length=35)

    def __str__(self):
        return self.name_in_english + " | " + self.name_in_arabic    
class Meals(models.Model):
    name_in_english = models.CharField(blank=True)
    name_in_arabic = models.CharField(blank=True)
    prices = models.CharField(verbose_name='Prices(to add new price add (|))', max_length=50, default=' | ')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='meals')
    # description_in_arabic = models.TextField(max_length=100, blank=True)
    # description_in_english = models.TextField(max_length=100, blank=True)
    meal_sales = models.IntegerField(blank=True , editable=True ,default=0)

    def clean(self):
        # Validate names
        if (self.name_in_arabic == '' and self.name_in_english) or (self.name_in_arabic and self.name_in_english == ''):
            raise ValidationError('Name in English and Arabic fields are required.')

        # Validate prices
        try:
            prices = [float(price.strip()) for price in self.prices.split('|') if price.strip()]
        except ValueError as e:
                raise ValidationError(f'Invalid price format. {str(e).split(":")[1]}')
    


    def __str__(self):
        return self.name_in_english + " | " + self.name_in_arabic

    class Meta:
        verbose_name = 'Meal'
        verbose_name_plural = 'Meals'

class Offers(models.Model):
    title = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='images/offers-img')
    def save(self, *args, **kwargs):
        try:
            this = Offers.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'
    def __str__(self):
        return self.title
class Admins(AbstractUser):
    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'
class Users(models.Model):
    username =  EncryptedCharField(max_length=35 , default='')
    city = EncryptedCharField(max_length=35 , default='')
    phone_number = EncryptedCharField(max_length=15 , default='')
    street_name = EncryptedCharField(max_length=35 , default='')
    email = EncryptedEmailField(default='')
    home_num = EncryptedIntegerField(default=0)
    Orders = models.IntegerField(default = 1 ,blank=True)
    last_order = models.DateTimeField()

    def save(self , *args , **kwargs):
        self.last_order = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    def __str__(self):
        return self.username
class Orders(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='orders')
    Order = models.TextField(max_length=500)
    total_price = models.DecimalField(max_digits=5 , decimal_places=2)
    order_date = models.DateTimeField()

    def save(self , *args , **kwargs):
        self.order_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Order
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
