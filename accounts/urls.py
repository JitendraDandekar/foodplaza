from django.urls import path
from .views import login, logout, register, view_customers, change_password

urlpatterns = [
	path('login/', login, name='login'),
	path('logout/', logout, name='logout'),
	path('register/', register, name='register'),
	path('view-customers/', view_customers, name='view-customers'),
	path('change-password/', change_password, name='change-password')
]