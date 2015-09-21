from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormView, View
from django.contrib.auth import authenticate, login, logout
from accounts.forms import RegisterForm, LoginForm
from django.contrib.auth.models import User

class RegisterFormView(FormView):
    form_class = RegisterForm
    success_url = "/login/"
    template_name = "accounts/front.register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

class LoginFormView(View):
    form_class = LoginForm
    success_url = "/user/%d/"
    template_name = "accounts/front.login.html"

    def get(self, request):
    	form = self.form_class(initial={ 'username': '', 'password': '' })
    	return render(request, self.template_name, {'form' : form, })

    def post(self, request):
    	form = self.form_class(request.POST)
    	if form.is_valid():
        	user = authenticate(username=form.cleaned_data['username'], 
        						password=form.cleaned_data['password'])
    		if user is not None:
    			login(request, user)
    			return HttpResponseRedirect(self.success_url % user.pk)

    	return render(request, self.template_name, {'form' : form })

class LogOutView(View):
	success_url = "/"

	def get(self, request):
		logout(request)
		return HttpResponseRedirect(self.success_url)
