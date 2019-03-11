from django.contrib import admin

from .models import Direction, Ingredient, Photo, Recipe


class PhotoInlineAdmin(admin.StackedInline):
    model = Photo
    extra = 2


class DirectionInlineAdmin(admin.TabularInline):
    model = Direction
    extra = 3


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('details',)


class IngredientInlineAdmin(admin.TabularInline):
    model = Ingredient
    extra = 6
    cached_choice_fields = ['direction',]

    def get_filters(self, obj):
        return ('direction', dict(recipe=obj),)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Only allow choosing directions from the directions that are in this recipe
        """
        field = super(IngredientInlineAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'direction':
            if request._obj_:
                field.queryset = field.queryset.filter(recipe=request._obj_)
            else:
                field.queryset = field.queryset.none()

        return field


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'prep_time',)
    fields = (
        'title', 'slug', 'category', 'description', 'serving_value', 'serving_string',
        'prep_time',)
    list_filter = ('title',)
    search_fields = ('title', 'description',)
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True
    model = Recipe
    inlines = [DirectionInlineAdmin, IngredientInlineAdmin, PhotoInlineAdmin]

    def get_form(self, request, obj=None, **kwargs):
        """
		just save obj reference for future processing in Inline
		"""
        request._obj_ = obj
        return super(RecipeAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Photo)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)

