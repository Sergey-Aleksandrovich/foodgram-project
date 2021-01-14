from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save

from recipes.utils import save_title_slug

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, )

    def __str__(self):
        return self.name


class IngredientList(models.Model):
    title = models.CharField(max_length=50)
    dimension = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.title},{self.dimension}'


class Ingredients(models.Model):
    kind = models.ForeignKey(IngredientList, on_delete=models.CASCADE,
                             related_name='ingredients')
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.kind.title} {self.quantity}, {self.kind.dimension}'


class Recipes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='recipes/')
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredients)
    tags = models.ManyToManyField(Tag, related_name='recipes')
    time = models.PositiveSmallIntegerField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    publication_date = models.DateTimeField('date published',
                                            auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title


class Follow(models.Model):
    following_date = models.DateTimeField('date follow',
                                          auto_now_add=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    def __str__(self):
        return f'follower-{self.user}->following-{self.author}'


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE,
                               related_name='favorites')

    def __str__(self):
        return f'user-{self.user}->recipe-{self.recipe}'


class Purchases(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='purchases')
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE,
                               related_name='purchases')

    def __str__(self):
        return f'user-{self.user}->recipe-{self.recipe}'


pre_save.connect(save_title_slug, sender=Recipes)
