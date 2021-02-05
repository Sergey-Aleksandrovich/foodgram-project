from django.views.generic import TemplateView


class AboutAuthorView(TemplateView):
    template_name = "author.html"


class AboutTechView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        type_list = [['Для создания сайта:', 'Django v:3.1.2', 'DRF v:3.12.2 ',
                      'Python v:3.7.6', 'PostgreSQL v:12.5', 'Javascript',
                      'HTML 5',
                      'CSS 3'],
                     ['Для разворачивания на боевом сервере:', 'Docker',
                      'Nginx', 'Gunicorn'],
                     ['Для автаматического деплоя:', 'GitHub workflow']]
        context['type_list'] = type_list
        return context

    template_name = "tech.html"


class AboutCatView(TemplateView):
    template_name = "photocat.html"


class AboutIView(TemplateView):
    template_name = "photoi.html"
