from django.contrib import admin
from .models import Meals, Category, Kind, Offers , Admins ,Users , Orders
from .forms import MealsForm , UserSignUpForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import DateFieldListFilter
from django.db.models import Sum, Count
from django.utils.html import format_html , mark_safe
from django.db.models.functions import TruncDate , TruncHour ,ExtractWeekDay  # Add this import
from django.core.cache import cache

# Customize admin site names
class MyAdminSite(admin.AdminSite):
    site_header = "Layali ElHelmia Administration"
    site_title = "Layali ElHelmia Admin Portal"
    index_title = "Welcome to the Layali ElHelmia Admin Panel"

    def index(self, request, extra_context=None):
        # Group orders by DATE (not datetime)
        sales_data = Orders.objects.annotate(
            truncated_date=TruncDate('order_date')  # Truncate to date
        ).values('truncated_date').annotate(
            total_sales=Sum('total_price'),
            order_count=Count('id')
        ).order_by('truncated_date')  # Order by truncated date

        time_sales_data = Orders.objects.annotate(
            truncated_hour=TruncHour('order_date')  # Group by hour
        ).values('truncated_hour').annotate(
            order_count=Count('id')
        ).order_by('truncated_hour')
        # Prepare chart data
        chart_labels = [entry['truncated_date'].strftime("%Y-%m-%d") for entry in sales_data]
        # Get total sales and order counts for each date
        sales_amounts = [float(entry['total_sales']) for entry in sales_data]
        order_counts = [entry['order_count'] for entry in sales_data]
        # get only top 5 meals and get thier needed information
        top_meals = Meals.objects.order_by('-meal_sales')[:5]
        top_meal_names = [meal.name_in_arabic for meal in top_meals]
        top_meal_sales = [meal.meal_sales for meal in top_meals]

        # Prepare time-based sales data
        time_order_counts_label = [entry['truncated_hour'].strftime("%H:%M") for entry in time_sales_data]
        time_order_counts_sales = [entry['order_count'] for entry in time_sales_data]
        
        # Prepare weekly sales data
        weekday_data = Orders.objects.annotate(
            weekday=ExtractWeekDay('order_date')  # Sunday=1, Saturday=7
        ).values('weekday').annotate(
            order_count=Count('id')
        ).order_by('weekday')

        day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 
                    'Thursday', 'Friday', 'Saturday']
        
        # Initialize with zeros for all days
        weekday_order_counts = [0] * 7
        for entry in weekday_data:
            day_index = entry['weekday'] - 1  # Convert to 0-based index
            weekday_order_counts[day_index] = entry['order_count']
        
        extra_context = {
            'chart_labels': chart_labels,
            'sales_amounts': sales_amounts,
            'order_counts': order_counts,
            'time_order_counts_label' : time_order_counts_label,
            'time_order_count_sales': time_order_counts_sales,
            'top_meal_names': top_meal_names,
            'top_meal_sales': top_meal_sales,
            'weekly_order_counts_label': day_names,
            'weekly_order_counts_sales': weekday_order_counts,
        }


        return super().index(request, extra_context)
# Register your custom admin site
admin_site = MyAdminSite(name='myadmin')
#make kind model TabularInline to category model
class kindINline(admin.TabularInline):
    model = Kind
    extra = 2
    # set max kinds for every category
    def get_max_num(self, request, obj=None, **kwargs):
        return 4

# tabularinline for Meal
class MealInline(admin.TabularInline):
    model = Meals
    extra = 0
    form = MealsForm
    #show only meal name 
    list_display = ['__str__']
    def get_min_num(self,request , obj=None , **kwargs):
        return 1


class CategoryAdmin(admin.ModelAdmin):
    #add kind and meal models to be inlines of category model
    inlines = [kindINline , MealInline]
    #show only category name and meals and kinds
    list_display = ['__str__' , 'show_kinds','show_meals']
    search_fields = ['__str__' , 'show_meals']
    # this two functions to show meals and kinds names
    def show_meals(self , obj):
        # get all objects of meal model
        meals = obj.meals.all()
        # show meals of category as a text string
        return '; '.join([str(meal.__str__()) + "| "+ str(meal.meal_sales) for meal in meals])
    # give name to column
    show_meals.short_description = 'Meals'  
    # The same thing to kinds
    def show_kinds(self , obj):
        kinds = obj.kinds.all()
        
        return ', '.join([kind.__str__() for kind in kinds])
    show_kinds.short_description = 'Kinds'
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        cache.clear()
# make usersadmin to show needed information like username ,
#  phone_number ,
#  Orders count ,
#  last_order date
class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone_number', 'Orders' , 'last_order']
    search_fields = ['username' , 'phone_number' , 'Orders']
    form = UserSignUpForm
# make the same thing to orders model to show  needed information like user ,
#  user_phone_number and order content ,
#  total price of order and order date 
# (all dates in dubai timezone you can see timezone in settings.py in line 110) 
# (TIME_ZONE = "Asia/Dubai")
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['formatted_order','total_price' ,'order_date', 'user' , 'user_phone_number']
    search_fields = ['user__username' , 'order_date' , 'user__phone_number' , 'Order' , 'total_price']
    list_filter = (
        ('order_date', DateFieldListFilter),
    )
    charts = [
        {
            'title': 'Sales Over Time (Total Revenue)',
            'type': 'line',
            'data_source': 'total_price',  # Field to aggregate (sum)
            'date_field': 'order_date',    # Group by date
            'func': 'sum',  # Explicitly sum the total_price values
        },
        {
            'title': 'Order Count Over Time',
            'type': 'bar',
            'data_source': 'id',  # Use 'id' to count orders
            'date_field': 'order_date',
            'func': 'count',  # Count the number of orders
        }

    ]
    

    def formatted_order(self, obj):
        return format_html('<br>'.join(obj.Order.split('\n')))
    formatted_order.short_description = 'Order'
    def user_phone_number(self , obj):
        return obj.user.phone_number
    user_phone_number.short_description = 'User Phone Number'
# show title of offer and image
class OffersAdmin(admin.ModelAdmin):
    list_display = ['__str__' , 'show_image']
    # show image in admin panel as an image tag  (you can see image in browser)
    def show_image(self , obj):
        return mark_safe('<img src="{}" width="100"/>'.format(obj.image.url))
    show_image.short_description = 'Image'
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        cache.clear()
# register all models with there ModelAdmins
admin_site.register(Category , CategoryAdmin)
admin_site.register(Admins , UserAdmin)
admin_site.register(Users, UsersAdmin)
admin_site.register(Orders , OrdersAdmin)
admin_site.register(Offers , OffersAdmin)
