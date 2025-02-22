from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
from .models import Meals, Category, Kind, Offers, Users, Orders  # Make sure to import the Users and Orders models
import csv
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
@csrf_protect
def homepage(request):
    offers = Offers.objects.all()
    return render(request, 'index.html', {'offers': offers})
@csrf_protect
def menu(request):
    meal_list = Meals.objects.all()
    categories = Category.objects.all()
    kinds = Kind.objects.all()
    category_kinds = {}
    
    for category in categories:
        category_kinds[category] = Kind.objects.filter(category=category)
    for meal in meal_list:
        meal.defaultprice = [price for price in meal.prices.split(' | ')][0]
        if float(meal.defaultprice.split('.')[1]) == 0:
            meal.defaultprice = int(float(meal.defaultprice))
        else:
            meal.defaultprice = float(meal.defaultprice)
    
    context = {
        'meals': meal_list,
        'categories': categories,
        'category_kinds': category_kinds,
    }
    # Render the menu page with the given context
    if request.path == '/menu/':
        return render(request, 'menu.html', context)
    elif request.path == '/menu_en/':
        return render(request,'menu_en.html', context)


@csrf_protect
def cart(request):
    content = {}
    
    # Check if the request method is POST
    if request.method == 'POST':  
        # Get the meals content from the POST request
        meals_list = request.POST.get('menuMealsContent')    
        # Get the order content from the POST request
        order = request.POST.get('ordercontent')
        
        # Get the total price from the POST request
        total_prices = request.POST.get('total_price')
        userinformation = {}
        selected_meals = ''
        
        # Check if username and phone number are provided in the POST request
        if request.POST.get('username') and request.POST.get('phone_number'):
            # Create a dictionary of user information excluding the CSRF token
            userinformation = {key: value for key, value in request.POST.items() if key != 'csrfmiddlewaretoken' and key!='ordercontent' and key!='total_price'}
            options = request.POST.get('options')
            # Get or create a user with the provided username and phone number
            # If the user was created, set the initial order count to 1
            filters = {}
            for field in ['username','phone_number', 'email', 'home_num', 'city', 'street_name']:
                if field in userinformation:
                    filters[field] = userinformation[field]

            # البحث عن مستخدم موجود بناءً على الفلتر (AND لجميع الحقول)
            user = Users.objects.filter(**filters).first()
            try:
                if user is None:
                    user = Users.objects.create(**userinformation, Orders=1)
            except Exception as e:
                pass
            else:
                user.Orders += 1
                user.save()
            if order:
                # Parse the order content to extract the meal names, quantities, prices, and options
                soup = BeautifulSoup(order, 'html.parser')
                # Extract the selected meals
                # Make list for all orders
                ordermeal_for_users = []
                ordermeal_for_admins = []
                # Iterate over the selected meals
                for meal_name_div , options ,count_div , price_div in zip(soup.find_all('p' , class_='mealname') ,
                soup.find_all('p' , class_='optionsvalue'),
                soup.find_all('p', class_='count'),
                soup.find_all('p' , class_='price')
                ):
                    if request.path == '/menu/cart/' or request.path == '/menu/cart':
                        meals = Meals.objects.filter(name_in_arabic=str(meal_name_div.text.strip()))  
                        if meals.exists():
                            meal = meals.first()
                            category_name_ar = meal.category.name_in_arabic
                            meal_name_ar = meal.name_in_arabic
                            category_name_en = meal.category.name_in_english
                            meal_name_en = meal.name_in_english
                    elif request.path == '/menu_en/cart_en/' or request.path == '/menu_en/cart_en':
                        meals = Meals.objects.filter(name_in_english=str(meal_name_div.text))  
                        if meals.exists():
                            meal = meals.first()
                            category_name_ar = meal.category.name_in_arabic
                            meal_name_ar = meal.name_in_arabic
                            category_name_en = meal.category.name_in_english
                            meal_name_en = meal.name_in_english
                    
                    count = int(count_div.text.strip()) if count_div else 'N/A'
                    price_meal = float(price_div.text.strip()) if price_div else 'N/A'
                    total_price = price_meal * count
                    # Iterate over the options
                    kind = str(options.text.strip()).split(' | ')[0] if options else 'N/A'
                    # Create the formatted string
                    # get all meal information but arabic information
                    if kind != 'None':
                        kind_text = f"{kind} :النوع" if kind else ""
                        order_detail = f"الوجبة: {category_name_ar} - {meal_name_ar} | الكمية: {str(count)}\nالسعر : {total_price} درهم اماراتي {kind_text}"
                        
                    else:
                        order_detail = f"الوجبة: {category_name_ar} - {meal_name_ar} | الكمية: {str(count)}\nالسعر : {total_price} درهم اماراتي"
                    # Append the formatted string to the ordermeal list
                    ordermeal_for_admins.append(order_detail)
                    if request.path == '/menu/cart/' or request.path == '/menu/cart':
                        if kind != 'None':
                            kind_text = f"{kind} :النوع" if kind else ""
                            order_detail = f"الوجبة: {category_name_ar} - {meal_name_ar} | الكمية: {str(count)}\nالسعر : {total_price} درهم اماراتي {kind_text}"
                            
                        else:
                            order_detail = f"الوجبة: {category_name_ar} - {meal_name_ar} | الكمية: {str(count)}\nالسعر : {total_price} درهم اماراتي"
                        # Append the formatted string to the ordermeal list
                        ordermeal_for_users.append(order_detail)
                    if request.path == '/menu_en/cart_en/' or request.path == '/menu_en/cart_en':
                        if kind != 'None':
                            kind_text = f"Kind: {kind}" if kind else ""
                            order_detail = f"Meal: {category_name_en} - {meal_name_en} | Count: {str(count)}\n {kind_text} Price: {total_price} AED"
                        else:
                            order_detail = f"Meal: {category_name_en} - {meal_name_en} | Count: {str(count)}\n Price: {total_price} AED"
                            # Append the formatted string to the ordermeal list
                        ordermeal_for_users.append(order_detail)
                # Create the formatted string for the order details
                order_details = '\n\n'.join(ordermeal_for_users)
                order_details_for_admins = '\n\n'.join(ordermeal_for_admins)
                # Create the order object
                Orders.objects.create(user=user, Order=order_details, total_price=float(total_prices))
                if order_details:
                    for order_detail in order_details.split('\n\n'):
                        meal_name = str(str(str(order_detail.split(':')[1]).split(' - ')[1]).split(' | ')[0])
                        count = int(str(str(order_detail.split(' | ')).split(': ')[2]).split('\\n')[0])
                        meal = Meals.objects.filter(name_in_arabic=meal_name).first()
                        if meal == None:
                            meal = Meals.objects.filter(name_in_english=meal_name).first()
                        if meal:
                            meal.meal_sales += count
                            meal.save()
                if request.path == '/menu/cart/' or request.path == '/menu/cart':
                    send_mail(
    'طلب من ليالي الحلمية',
    f"""
    {user.username} عزيزي,
    \nشكرًا لطلبك من ليالي الحلمية. تم استلام طلبك بتاريخ 
    {timezone.now().strftime('%Y-%m-%d')}، وسيتم التواصل معك لتأكيد التفاصيل.
    
    تفاصيل الطلب:

    {order_details}


    السعر الاجمالي: {total_prices} درهم اماراتي

    +971 55 424 1799 :خدمه العملاء
    """,
    settings.EMAIL_HOST_USER,
    [user.email]
    )   
                elif request.path == '/menu_en/cart_en/' or request.path == '/menu_en/cart_en':
                    send_mail(
    'Order from Layali Al Helmeya',
    f"""
    Dear {user.username},

    Thank you for your order from Layali Al Helmeya. Your order has been received on 
    {timezone.now().strftime('%Y-%m-%d')}, and we will contact you to confirm the details.
                    
    Order details:

    {order_details}

    Total price: {total_prices} AED

    Customer Service: +971 55 424 1799
    """,
    settings.EMAIL_HOST_USER,
    [user.email]
                )

                send_mail('طلب جديد',
    f"""
    تم استلام طلب جديد بتاريخ 
    {timezone.now().strftime('%Y-%m-%d')}   

    اسم العميل:
    {user.username}

    رقم الهاتف:
    {user.phone_number}

    العنوان:
    {user.city}-{user.home_num}-{user.street_name}

    :تفاصيل الطلب

    {order_details_for_admins}

    السعر الاجمالي: {total_prices} درهم اماراتي
    """,
    settings.EMAIL_HOST_USER,
    ['mina.alber127@gmail.com'],#you can replace this email or add comma and add
    # your email if you want to try
    #After trying you should reset meals sales , you can type /reset_meals_sales/ 
    # in the link
    )


        if meals_list:                   
            soup = BeautifulSoup(meals_list , 'html.parser')
            meal_divs = soup.find_all('div' , class_ = 'menuType')
            selected_meals = ''
            for div in meal_divs:
                meal_id = div['id']
                price = str(div.find('p' , class_ = 'price').text.strip())
                
                prices = str(div.find('select')['onchange'].split(',')[1].replace('\r\n                     ' ,'')).replace('\'' , '')
                if price in prices:
                    if Meals.objects.filter(id=meal_id):
                        if Meals.objects.filter(prices=prices):  
                            selected_meals = selected_meals + str(div)
                                    

                


            content = {'meals': selected_meals}
    
    if request.path == '/menu_en/cart_en/' or request.path == '/menu_en/cart_en':
        return render(request , 'cart_en.html', content)
    if request.path == '/menu/cart/' or request.path == '/menu/cart':
        return render(request , 'cart.html', content)
@csrf_protect
def reset_meals_sales(request):
    meals = Meals.objects.all()
    for meal in meals:
        meal.meal_sales = 0
        meal.save()
    return HttpResponse('Done')