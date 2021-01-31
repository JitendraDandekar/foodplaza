from django.shortcuts import render, redirect
from .forms import FoodForm
from .models import Food, Cart
from accounts.models import Customer
from accounts.forms import ContactForm
from django.http import JsonResponse
from django.db import connection
import json
from accounts.views import autherized_page

# Create your views here.
def show_foods(request):
	foods = Food.objects.all()
	context = { 'foods': foods }
	return render(request, 'foods/show-foods.html', context)


@autherized_page
def edit_foods(request):
	foods = Food.objects.all()
	context = { 'foods': foods }
	return render(request, 'foods/edit-foods.html', context)


@autherized_page
def add_food(request):
	form = FoodForm()

	if request.method == 'POST':
		form = FoodForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('edit-foods')

	context = { 'form': form }
	return render(request, 'foods/add-food.html', context)


@autherized_page
def update_food(request, pk):
	food = Food.objects.get(id=pk)
	form = FoodForm(instance=food)

	if request.method == 'POST':
		form = FoodForm(request.POST, request.FILES, instance=food)
		if form.is_valid():
			form.save()
			return redirect('edit-foods')

	context = { 'form': form }
	return render(request, 'foods/add-food.html', context)


@autherized_page
def delete_food(request, pk):
	food = Food.objects.get(id=pk)
	food.delete()
	return redirect('edit-foods')


def add_to_cart(request):
	user = Customer.objects.get(id=request.session['customer'])
	food = Food.objects.get(id=request.GET.get('product_id'))
	Cart.objects.create(customer=user, food=food, quantity=1, price=food.price)
	return JsonResponse('Added Successfully!', safe=False)


def cart(request):
	customer = Customer.objects.get(id=request.session['customer'])
	contactform = ContactForm(instance=customer)
	if request.method == 'POST':
		contactform = ContactForm(request.POST, instance=customer)
		if contactform.is_valid():
			contactform.save()
			return redirect('cart')
	context = { 'name': customer.name, 'contact': customer.contact, 'address': customer.address, 'contactform': contactform }
	return render(request, 'foods/cart.html', context)


def view_cart(request):
	customer_id = request.session['customer']
	with connection.cursor() as cursor:
		cursor.execute("""select c.id as id, f.title as title, f.quantity as food_quantity, f.price as food_price, 
			c.quantity as cart_quantity, c.price as cart_price from cart c inner join food f 
			on f.id=c.food_id where c.customer_id=%s and c.orderd=false;""", (customer_id,))
		rows = cursor.fetchall()
	columns = ( 'id', 'title', 'food_quantity', 'food_price', 'cart_quantity', 'cart_price')	
	cart = []
	for row in rows:
		cart.append(dict(zip(columns, row)))
	if len(cart) == 0:
		return JsonResponse({'status':'false'}, status=404)
	return JsonResponse(cart, safe=False)


def delete_cart(request):
	cart_id = request.GET.get('cart_id')
	cart = Cart.objects.get(id=cart_id)
	cart.delete()
	return JsonResponse('Deleted Successfully!', safe=False)


def place_order(request):
	cart = request.POST.get('cart')
	json_cart = json.loads(cart)
	for i in json_cart:
		Cart.objects.filter(id=i['cart_id']).update(quantity=i['cart_quantity'], price=i['cart_price'], orderd=True)
	return JsonResponse('Order Placed!', safe=False)


def ordered_food(request):
	customer_id = request.session['customer']
	with connection.cursor() as cursor:
		cursor.execute("""select c.id as id, f.title as title, c.quantity as cart_quantity, c.price as cart_price, 
			c.date as ordered_date, c.delivered as delivery from cart c inner join food f on f.id=c.food_id 
			where c.customer_id=%s and c.orderd=true order by c.date desc;""", (customer_id,))
		rows = cursor.fetchall()
	ordered = []
	columns = ('id', 'title', 'cart_quantity', 'cart_price', 'ordered_date', 'delivery',)
	for row in rows:
		ordered.append(dict(zip(columns, row)))
	if len(ordered) == 0:
		return JsonResponse({'status':'false'}, status=404)
	return JsonResponse(ordered, safe=False)


def orders(request):
	with connection.cursor() as cursor:
		cursor.execute("""select cust.name, cust.contact, cust.address, f.title, c.quantity, c.price, c.date, c.delivered from customer cust inner join cart c on cust.id=c.customer_id inner join food f
			on c.food_id=f.id where c.orderd=true order by c.date desc;""")
		rows = cursor.fetchall()
	columns = ('name', 'contact', 'address', 'title', 'quantity', 'price', 'date', 'delivered')
	orders = []
	for row in rows:
		orders.append(dict(zip(columns, row)))
	context = {'orders': orders}
	return render(request, 'foods/orders.html', context)