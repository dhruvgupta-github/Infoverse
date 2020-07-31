from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name= 'index.html'

class TestPage(TemplateView):
    template_name= 'test.html'

class ThanksPage(TemplateView):
    template_name='thanks.html'

class AboutPage(TemplateView):
    template_name='more/about.html'

class FeaturePage(TemplateView):
    template_name='more/features.html'

class DeveloperPage(TemplateView):
    template_name='more/developer.html'