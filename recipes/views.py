import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View
from fpdf import FPDF

from .forms import RecipesForm
from .models import IngredientList, Ingredients, Recipes, Favorites, User, \
    Follow, Purchases


class PDF(FPDF):
    def header(self):
        self.image('logo.jpg', 10, 8, 33)
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 15)
        self.cell(80)
        self.cell(30, 10, 'Список ингредиентов', 0, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', style='', size=8, )
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def create_dict_ingredients(request):
    result = dict()
    purchases = Purchases.objects.filter(
        user=request.user).select_related('recipe').order_by(
        '-pk')
    for purchase in purchases:
        for ingredient in purchase.recipe.ingredients.all():
            if result.get(ingredient.kind.title):
                result[ingredient.kind.title] = [
                    result[ingredient.kind.title][0] + ingredient.quantity,
                    ingredient.kind.dimension]
            else:
                result[ingredient.kind.title] = [ingredient.quantity,
                                                 ingredient.kind.dimension]
    return result


def request_add_ingredients(data):
    data._mutable = True
    data['ingredients'] = []
    for key in data.keys():
        if key[:15] == 'nameIngredient_':
            index_number = key[15:]
            data['ingredients'].append(
                [data['nameIngredient_' + index_number],
                 data['valueIngredient_' + index_number],
                 data['unitsIngredient_' + index_number]])
    return data


def check_tegs(request):
    result = []
    if request.GET.get('breakfast') == 'True':
        result.append(1)
    if request.GET.get('lunch') == 'True':
        result.append(2)
    if request.GET.get('dinner') == 'True':
        result.append(3)
    return result


@login_required
def ingredients_list(request):
    if request.method == 'GET' and request.GET['query']:
        ingredients = list(IngredientList.objects.filter(
            title__istartswith=request.GET['query']).values())
    else:
        ingredients = None
    return JsonResponse(ingredients, safe=False)


def index_view(request):
    tags = check_tegs(request)
    recipe_list = Recipes.objects.filter(tags__in=tags).select_related(
        'author').order_by(
        '-publication_date').all().distinct()
    if request.user.is_authenticated:
        favorites_recipes = Recipes.objects.filter(
            favorites__user=request.user)
        purchases_recipes = Recipes.objects.filter(
            purchases__user=request.user)
    else:
        purchases_recipes = tuple()
        favorites_recipes = tuple()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html',
                  {'page': page, 'paginator': paginator,
                   'favorites_recipes': favorites_recipes,
                   'purchases_recipes': purchases_recipes})


def profile_view(request, username):
    tags = check_tegs(request)
    author = get_object_or_404(User, username=username)
    recipe_list = Recipes.objects.filter(tags__in=tags,
                                         author=author).select_related(
        'author').order_by(
        '-publication_date').all().distinct()
    if request.user.is_authenticated:
        favorites_recipes = Recipes.objects.filter(
            favorites__user=request.user)
        following = Follow.objects.filter(user=request.user,
                                          author=author).exists()
    else:
        favorites_recipes = tuple()
        following = False
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'Profile.html',
                  {'page': page, 'paginator': paginator,
                   'favorites_recipes': favorites_recipes,
                   'author': author, 'following': following})


def recipe_view(request, slug):
    recipe = get_object_or_404(Recipes, slug=slug)
    if request.user.is_authenticated:
        favorites = Favorites.objects.filter(user=request.user,
                                             recipe=recipe)
        following = Follow.objects.filter(user=request.user,
                                          author=recipe.author)
        purchase = Purchases.objects.filter(user=request.user, recipe=recipe)

    else:
        favorites = False
        following = False
        purchase = False

    return render(request, 'SinglePage.html',
                  {'favorite': favorites, 'recipe': recipe,
                   'following': following, 'purchase': purchase})


@login_required
def purchases_download_view(request):
    dict_ingredients = create_dict_ingredients(request)
    filename = request.user
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)
    for ingredient in dict_ingredients:
        pdf.cell(0, 10,
                 f'{ingredient} {dict_ingredients[ingredient][0]},'
                 f' {dict_ingredients[ingredient][1]}', 1, 1)
    response = HttpResponse(
        pdf.output(f'shopping_list_{filename}.pdf', 'S').encode('latin-1'),
        'application/pdf')
    response['Content-Disposition'] = \
        f'attachment; ' \
        f'filename="shopping_list_{filename}.pdf"'
    return response


@login_required
def recipe_edit_view(request, slug):
    author = get_object_or_404(User, username=request.user)
    recipe = get_object_or_404(Recipes, slug=slug, author=author)
    if not recipe:
        return redirect(f'/{slug}')
    form = RecipesForm(request.POST or None, files=request.FILES or None,
                       instance=recipe)
    if request.method == 'POST':
        form = RecipesForm(request_add_ingredients(request.POST) or None,
                           files=request.FILES or None, instance=recipe)

        if form.is_valid():
            recipe_form = form.save(commit=False)
            recipe.ingredients.clear()
            recipe.tags.clear()
            for ingredient in form.cleaned_data['ingredients']:
                ingredient_model = Ingredients.objects.filter(
                    kind=IngredientList.objects.get(title=ingredient[0]),
                    quantity=ingredient[1])
                if ingredient_model.exists():
                    recipe_form.ingredients.add(ingredient_model[0].pk)
                else:
                    ingredient_model = Ingredients.objects.create(
                        kind=IngredientList.objects.get(title=ingredient[0]),
                        quantity=ingredient[1])
                    recipe_form.ingredients.add(ingredient_model.pk)
            tags = form.cleaned_data['tags']
            recipe_form.tags.add(*tags)
            recipe_form.save()
            return redirect(f'/recipe/{slug}')
    return render(request, 'formRecipe.html', {'form': form, 'recipe': recipe})


@method_decorator(login_required, name='dispatch')
class FavoriteView(View):
    template_name = 'Favorites.html'

    def get(self, request, *args, **kwargs):
        tags = check_tegs(request)
        recipe_list = Recipes.objects.filter(tags__in=tags,
                                             favorites__user=request.user) \
            .select_related('author') \
            .order_by('-publication_date') \
            .all().distinct()
        if request.user.is_authenticated:
            favorites_recipes = Recipes.objects.filter(
                favorites__user=request.user)
            purchases_recipes = Recipes.objects.filter(
                purchases__user=request.user)
        else:
            favorites_recipes = tuple()
            purchases_recipes = tuple()
        paginator = Paginator(recipe_list, 6)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request, self.template_name,
                      {'page': page, 'paginator': paginator,
                       'favorites_recipes': favorites_recipes,
                       'purchases_recipes': purchases_recipes})

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        recipe_id = body['id']
        recipe = get_object_or_404(Recipes, pk=recipe_id)
        Favorites.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse("succes", safe=False)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipes, pk=recipe_id)
        favorite = Favorites.objects.filter(user=request.user, recipe=recipe)
        if favorite:
            favorite.delete()
            return JsonResponse("succes", safe=False)
        return HttpResponse(status=403)


@method_decorator(login_required, name='dispatch')
class PurchasesView(View):
    template_name = 'ShopList.html'

    def get(self, request, *args, **kwargs):
        purchases = Purchases.objects.filter(
            user=request.user).select_related('recipe').order_by(
            '-pk')
        return render(request, self.template_name,
                      {'purchases': purchases, })

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        recipe_id = body['id']
        recipe = get_object_or_404(Recipes, pk=recipe_id)
        Purchases.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse("succes", safe=False)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipes, pk=recipe_id)
        purchase = Purchases.objects.filter(user=request.user, recipe=recipe)
        if purchase:
            purchase.delete()
            return JsonResponse("succes", safe=False)
        return HttpResponse(status=403)


class FollowView(View):
    template_name = 'MyFollow.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        follows = Follow.objects.select_related('author').filter(
            user=request.user).order_by('-following_date')
        author = []
        for follow in follows:
            author.append(follow.author)
        paginator = Paginator(follows, 6)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request, self.template_name,
                      {'page': page, 'paginator': paginator, })

    @method_decorator(login_required)
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        author_id = body['id']
        Follow.objects.get_or_create(user=request.user, author_id=author_id)
        return JsonResponse("succes", safe=False)

    @method_decorator(login_required)
    def delete(self, request, author_id):
        author = get_object_or_404(User, pk=author_id)
        follow = Follow.objects.filter(user=request.user, author=author)
        if follow:
            follow.delete()
            return JsonResponse("succes", safe=False)
        return HttpResponse(status=403)


class RecipesFormView(View):
    form_class = RecipesForm
    template_name = 'formRecipe.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        print(request.POST)
        new_request_post = request_add_ingredients(request.POST)
        form = self.form_class(new_request_post, files=request.FILES)

        if form.is_valid():
            recipes = form.save(commit=False)
            recipes.author = request.user
            recipes.save()
            for ingredient in form.cleaned_data['ingredients']:
                ingredient_model = Ingredients.objects.filter(
                    kind=IngredientList.objects.get(title=ingredient[0]),
                    quantity=ingredient[1])
                if ingredient_model.exists():
                    print(recipes)
                    recipes.ingredients.add(ingredient_model[0].pk)
                else:
                    ingredient_model = Ingredients.objects.create(
                        kind=IngredientList.objects.get(title=ingredient[0]),
                        quantity=ingredient[1])
                    recipes.ingredients.add(ingredient_model.pk)
            tags = form.cleaned_data['tags']
            recipes.tags.add(*tags)
            return redirect('creation_recipe_success')
        else:
            return render(request, self.template_name, {'form': form})


class RecipesFormViewSuccess(TemplateView):
    template_name = "creation_recipe_done.html"
