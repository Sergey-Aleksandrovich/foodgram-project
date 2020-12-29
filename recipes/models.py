import random
import string

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify as django_slugify

# TODO: посмотреть правильный порядок импортов, и добавить модель рецептов!
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


alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
            'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
            'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh',
            'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def slugify(s):
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))


def random_string_generator(size=10,
                            chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:

        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def save_title_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(save_title_slug, sender=Recipes)
