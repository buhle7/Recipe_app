import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Recipe(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Recipe|title'))
    cooking_time = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=5, null=False, blank=False)
    prep_time = models.CharField(max_length=100, blank=True)
    serving_value = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(default=0, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipies')

    def save(self):
        self.modified_time = datetime.datetime.now()
        self.scale = 1.0
        super(Recipe, self).save()


class Direction(models.Model):
    """
    A direction is a step in a recipe's preparation and each recipe can have
    multiple directions but obviously, each direction only applies to one
    recipe.
    """
    text = models.TextField(blank=True, verbose_name=_('Direction|text'))
    recipe = models.ForeignKey(Recipe, related_name='directions', on_delete=models.CASCADE)


    def __str__(self):
        ret = self.text[:40]
        if len(self.text) > 40:
            ret += "..."
        return ret

    class Meta:
        verbose_name = _('Direction')
        verbose_name_plural = _('Directions')
        ordering = ['id']


class Ingredient(models.Model):
    details = models.CharField(max_length=500, blank=True, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    direction = models.ForeignKey(Direction, related_name='ingredients', null=True, blank=True,
                                  on_delete=models.SET_NULL)

    class Meta:
        ordering = ["direction", "id"]
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')


class Photo(models.Model):
    recipe = models.ForeignKey('Recipe', null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='images')

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')
