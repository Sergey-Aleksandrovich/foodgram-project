from django.views.generic import TemplateView


class AboutAuthorView(TemplateView):
    template_name = "author.html"


class AboutTechView(TemplateView):
    template_name = "tech.html"


class AboutCatView(TemplateView):
    template_name = "photocat.html"


class AboutIView(TemplateView):
    template_name = "photoi.html"