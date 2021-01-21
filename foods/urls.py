from django.urls import path
from .views import edit_foods, add_food, update_food, delete_food, show_foods, add_to_cart, cart, view_cart, delete_cart, place_order, ordered_food

urlpatterns = [
	path('', show_foods, name='show-foods'),
	path('edit-foods/', edit_foods, name='edit-foods'),
	path('add-food/', add_food, name='add-food'),
	path('update-food/<int:pk>/', update_food, name='update-food'),
	path('delete-food/<int:pk>/', delete_food, name='delete-food'),
	path('add-to-cart/', add_to_cart, name='add-to-cart'),
	path('cart/', cart, name='cart'),
	path('view-cart/', view_cart, name='view-cart'),
	path('delete-cart/', delete_cart, name='delete-cart'),
	path('place-order/', place_order, name='place-order'),
	path('ordered-food/', ordered_food, name='ordered-food'),
]