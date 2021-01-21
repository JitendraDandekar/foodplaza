from django.db import models

# Create your models here.
class Customer(models.Model):
	name = models.CharField(max_length=100)
	email = models.CharField(max_length=100, unique=True)
	contact = models.IntegerField()
	address = models.CharField(max_length=100)
	password = models.CharField(max_length=100)

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'customer'


class Admin(models.Model):
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=100)

	def __str__(self):
		return self.username

	class Meta:
		db_table = 'admin'