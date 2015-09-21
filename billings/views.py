from django.shortcuts import render
from django.views.generic.edit import View
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError, Http404
from django.contrib.auth.models import User
from billings.forms import BillingForm
from billings.helpers import set_cookie, gen_password, validate_permissions, perform_query
from billings.crypto import DESCryptor
from billings.validate import TransactionValidator
from billings.models import ValidatedTransaction

# Create your views here.

class CreateBilling(View):
	form_class = BillingForm
	default_cryptor = DESCryptor
	default_validator = TransactionValidator
	success_url = "/user/%d/"
	template_name = "billings/personal.billing.html"

	def get(self, request):
		form = self.form_class(initial={ 'bid': '0', 'sign': '' })
		return render(request, self.template_name, {'form' : form, })

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			if request.user.is_authenticated():
				billing = form.save(commit=False)
				billing.user = request.user
					
				_cryptor = self.default_cryptor(*gen_password(request.user.password))

				try:
					billing.sign = billing.sign[:70]
					billing.sign = _cryptor.encrypt(billing.sign.encode('ascii'))
				except Exception as ex:
					return HttpResponseServerError(str(ex).encode('utf-8'))

				billing.transaction_timestamp = timezone.now()
				billing.save()

				_validator = self.default_validator()

				try:
					trz_sign = _validator.invalidate(request.user.username, billing.sign)
				except Exception as ex:
					return HttpResponseServerError(str(ex).encode('utf-8'))

				response = HttpResponseRedirect(self.success_url % request.user.id)
				set_cookie(response, 'transaction_sign', trz_sign)
				set_cookie(response, 'transaction_id', billing.sign)
				return response
			else:
				form.add_error(None, "User must be logged in to create billings")		
		return render(request, self.template_name, {'form' : form })


class CheckTransaction(View):
	default_cryptor = DESCryptor

	def get(self, request, name):
		user = User.objects.get(username__iexact=name)
		transaction_id = request.COOKIES.get('transaction_id')
		if transaction_id is not None:

			passwd = gen_password(user.password)
			_cryptor = self.default_cryptor(*passwd)

			try:
				sign = _cryptor.decrypt(transaction_id)
			except Exception as ex:
				return HttpResponseServerError(str(ex).encode('utf-8'))
				
			if validate_permissions(request.user, name):
				return HttpResponse(sign)
			else:
				raise Http404("User don't have permissions to check this transaction")
		else:
			raise Http404("Transaction id is empty")

class ValidateTransaction(View):
	default_validator = TransactionValidator
	template_name = "billings/personal.status.html"

	def query_transaction(self, tid):
		transaction = perform_query(
				ValidatedTransaction, 
				"select * from billings_validatedtransaction where tranzaction_id = '%s'" % tid)
		return transaction

	def get(self, request, tid):

		transaction = self.query_transaction(tid)
		transaction_sign = request.COOKIES.get('transaction_sign')
		if transaction_sign is not None:

			try:
				_validator = self.default_validator()
				if _validator.validate(transaction, transaction_sign):
					resp = render(request, self.template_name, {"transaction": transaction, "status":"validated"})
					set_cookie(resp, "valid", "True")
					return resp
				else:
					return render(request, self.template_name, {"transaction": transaction, "status":"unvalidated"})
			except Exception as ex:
				return HttpResponseServerError(ex)
		else:
			raise Http404("Transaction sign is empty")
