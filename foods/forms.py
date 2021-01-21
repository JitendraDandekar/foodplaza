from django import forms
from .models import Food

class FoodForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	quantity = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

	class Meta:
		model = Food
		fields = ['title', 'quantity', 'category', 'price', 'image']