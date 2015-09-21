from django.views.generic.base import TemplateView

class IndexPage(TemplateView):
	template_name = "front.index.html"

class RulesPage(TemplateView):
	template_name = "front.rules.html"