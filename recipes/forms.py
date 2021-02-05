from django.core.exceptions import ValidationError
from django.forms import ModelForm, forms

from .models import IngredientList, Recipes


class IngredientsField(forms.Field):
    def clean(self, value):
        if isinstance(value, list):
            return value
        raise ValidationError(f'Необходимо ввести ингредиенты')


class RecipesForm(ModelForm):
    ingredients = IngredientsField(label='Ингредиенты')

    class Meta:
        model = Recipes
        fields = (
            'title', 'tags', 'ingredients', 'time', 'description', 'image')
        labels = {'title': 'Название рецепта',
                  'tags': 'Теги',
                  'time': 'Время приготовления',
                  'description': 'Описание',
                  'image': 'Загрузить фото'
                  }

    def clean_ingredients(self):
        set_ingredients = set()
        ingredients_form = self.cleaned_data['ingredients']
        print(ingredients_form)
        ingredients_db = list(IngredientList.objects.values('title'))
        for ingredient_form in ingredients_form:
            set_ingredients.add(ingredient_form[0])
            for ingredient_db in ingredients_db:
                if int(ingredient_form[1]) <= 0:
                    raise ValidationError(
                        "Количество ингредиента должно быть больше 0")
                if ingredient_db['title'] == ingredient_form[0]:
                    break
                if ingredients_db[-1] == ingredient_db:
                    raise ValidationError(
                        "Выберите ингредиент из выпадающего списка")
        if len(set_ingredients) is not len(ingredients_form):
            raise ValidationError(
                "Выбирайте ингредиет только один раз")
        return ingredients_form
