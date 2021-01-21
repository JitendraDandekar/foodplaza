from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from .models import Admin, Customer
from .forms import CustomerForm
from django.http import JsonResponse, HttpResponse

# Create your views here.
def autherized_page(func):
	def inner(request, *args, **kwargs):
		try:
		 	if request.session['admin']:
		 		return func(request, *args, **kwargs)
		except:
			return HttpResponse('<h1>Unauthorized Page</h1');
	return inner


def index(request):
	return render(request, 'index.html')


def login(request):
	if request.method == 'POST':
		user = request.POST['user']
		username = request.POST['username']
		password = request.POST['password']

		if user == 'admin':
			with connection.cursor() as cursor:
				cursor.execute("select id from admin where username=%s and password=%s", (username, password))
				user = cursor.fetchone()
			
			if user is not None:
				request.session['admin'] = user[0]
				return redirect('index')
			else:
				messages.error(request, 'Invalid Credentials!')
				return redirect('login')


		elif user == 'customer':
			with connection.cursor() as cursor:
				cursor.execute("select id, name from customer where email=%s and password=%s", (username, password))
				user = cursor.fetchone()
	
			if user is not None:
				request.session['customer'] = user[0]
				request.session['customer_name'] = user[1]
				return redirect('index')
			else:
				messages.error(request, 'Invalid Credentials!')
				return redirect('login')

	return render(request, 'accounts/login.html')


def logout(request):
	try:
		del request.session['admin']
	except KeyError:
		pass
	try:
		del request.session['customer']
	except KeyError:
		pass
	return redirect('index')


def register(request):
	form = CustomerForm()

	if request.method == 'POST':
		form = CustomerForm(request.POST)
		if form.is_valid():
			password = form.cleaned_data['password']
			confirm_password = form.cleaned_data['confirm_password']
			if password == confirm_password:
				form.save()
				return redirect('login')
			else:
				messages.error(request, 'Password Not Matched!')
				return redirect('register')

	context = { 'form': form }
	return render(request, 'accounts/register.html', context)


@autherized_page
def view_customers(request):
	with connection.cursor() as cursor:
		cursor.execute('select id, name, email, contact, address from customer;')
		rows = cursor.fetchall()
	columns = ('id', 'name', 'email', 'contact', 'address')
	customers = []
	for row in rows:
		customers.append(dict(zip(columns, row)))
	context = { 'customers': customers }
	return render(request, 'accounts/customer.html', context)




