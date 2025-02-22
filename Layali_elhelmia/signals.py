from django.db.models.signals import post_delete , post_save
from django.dispatch import receiver
from .models import Meals ,Kind, Category , Offers , Orders , Users
import os

# delete image if category , offers has been deleted
@receiver(post_delete, sender=Category)
@receiver(post_delete , sender=Offers)
def delete_image_on_category_delete(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
    if instance.image:
        img_path = instance.image.path
        img = Image.open(img_path)
        img = img.convert("RGB")
        img.save(img_path, format="JPEG", quality=70, optimize=True)
# split prices 
@receiver(post_save, sender=Meals)
def convert_to_float(sender, created, instance, **kwargs):
    if not hasattr(instance, '_prices_converted'):
        if instance.prices != '|':
            prices_instance = [str(float(price.replace(' ', ''))) for price in instance.prices.split('|') if price != '']
            instance.prices = ' | '.join(prices_instance)
            instance._prices_converted = True
            instance.save()
        else:
            instance.delete()
@receiver(post_delete , sender=Orders)
def delete_meal_counts(sender,  instance, **kwargs):
    meal_name=''
    count = 0
    try:
        if instance.Order:
            for order_detail in instance.Order.split('\n\n'):
                meal_name = str(str(str(order_detail.split(':')[1]).split(' - ')[1]).split(' | ')[0])
                count = int(str(str(order_detail.split(' | ')).split(': ')[2]).split('\\n')[0])
                meal = Meals.objects.filter(name_in_arabic=meal_name).first()
                if meal == None:
                    meal = Meals.objects.filter(name_in_english=meal_name).first()
                if meal:
                    if meal.meal_sales > 0:
                        meal.meal_sales -= count
                        if meal.meal_sales < 0:
                            meal.meal_sales = 0
                        meal.save()
    except Exception as e:
        pass