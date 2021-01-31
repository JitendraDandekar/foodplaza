from django.db import models
from accounts.models import Customer

# Create your models here.
class Food(models.Model):
	title = models.CharField(max_length=100)
	image = models.ImageField(upload_to='foods/')
	category = models.CharField(max_length=100)
	quantity = models.CharField(max_length=100)
	price = models.FloatField()

	def __str__(self):
		return self.title

	class Meta:
		db_table = 'food'


class Cart(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	food = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField()
	price = models.FloatField()
	orderd = models.BooleanField(default=False)
	delivered = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.customer.name

	class Meta:
		db_table = 'cart'
