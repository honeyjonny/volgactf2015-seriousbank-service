from django import forms
from billings.models import AccountBilling

class BillingForm(forms.ModelForm):
	bid = forms.IntegerField(
		label="Bid value", 
		min_value=1, 
		max_value=100500, 
		widget=forms.NumberInput(
			attrs={'class' : 'form-control',
			'style':'margin-left:5%'}))
	sign = forms.CharField(
		label="CVC", 
		max_length=70, 
		widget=forms.TextInput(
			attrs={'class' : 'form-control',
			'style':'margin-left:5%'}))
	class Meta:
		model = AccountBilling
		fields = ('bid', 'sign',)
