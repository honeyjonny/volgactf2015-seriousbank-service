from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from billings.models import AccountBilling
# Create your views here.

class UserHomePage(TemplateView):
	template_name = "cabinet/personal.cabinet.html"
	user = None

	def get(self, request, index, *args, **kwargs):
		try:
			self.user = User.objects.get(pk=index)
		except Exception as ex:
			raise Http404("User not found")

		context = self.get_context_data(**kwargs)
		return self.render_to_response(context)

	def get_context_data(self, **kwargs):
		ctx = super(UserHomePage, self).get_context_data(**kwargs)
		if self.user is not None:
			query = AccountBilling.objects.filter(user_id=self.user.id)
			ctx['username'] = self.user.username
			ctx['account_summary'] = reduce(lambda acc, item: acc + item.bid, query, 0)
			ctx['billing_story'] = query.order_by("-transaction_timestamp")
		return ctx
