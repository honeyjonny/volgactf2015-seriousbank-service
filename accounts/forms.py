from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
	username = forms.CharField(
		label="username", 
		max_length=50, 
		widget=forms.TextInput(
			attrs={'class' : 'form-control'}))
	password = forms.CharField(
		label="password", 
		max_length=50, 
		widget=forms.PasswordInput(
			attrs={'class' : 'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'password',)

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user

class LoginForm(forms.Form):
	username = forms.CharField(
		label="username", 
		max_length=50, 
		widget=forms.TextInput(
			attrs={'class' : 'form-control'}))
	password = forms.CharField(
		label="password", 
		max_length=50, 
		widget=forms.PasswordInput(
			attrs={'class' : 'form-control'}))