from django import template

from recipes.models import Favorites

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def addclassrow(field, args):
    arg_list = [arg.strip() for arg in args.split(',')]
    return field.as_widget(attrs={"class": arg_list[0],
                                  "row": arg_list[1]})

@register.filter
def favorite(recipe, request_user):
    if Favorites.objects.filter(recipe=recipe, user=request_user).exists():
        return True
    return False
