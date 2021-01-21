from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):	
	name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
	contact = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'input_type': 'password', 'class': 'form-control'}))
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'input_type': 'password', 'class': 'form-control'}))

	class Meta:
		model = Customer
		fields = ['name', 'email', 'contact', 'address', 'password', 'confirm_password']


class ContactForm(forms.ModelForm):
	contact = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}))

	class Meta:
		model = Customer
		fields = ['contact', 'address']