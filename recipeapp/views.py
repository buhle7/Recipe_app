from random import randint
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Recipe, Ingredient, Direction, Photo


# Request methods
def index(request):
    recipes = Recipe.objects.select_related().all()[:25]
    data = {
        'recipes': recipes
    }
    return render(request, 'index.html', context=data)


def recipe_details(request, id):
    recipe = Recipe.objects.select_related('').get(id=id)
    data = {
        'recipe': recipe
    }
    return render(request, 'details.html', context=data)


def create_recipe(request):
    print(request)
    if request.method == 'POST':
        title = request.POST['title']
        prep = request.POST['prep_time']
        slug = title[:3] + str(randint(0, 9))
        cook_time = request.POST['cooking_time']
        serving = request.POST['servings']
        photo = request.FILES['photo']
        rating = request.POST['rating']
        ingredients = request.POST['ingredients']
        cook_instr = request.POST['cooking_instructions']

        recipe = Recipe(title=title, prep_time=prep, cooking_time=cook_time, serving_value=serving, rating=rating,
                        slug=slug)
        recipe.save()

        ingredients = Ingredient(details=ingredients, recipe=recipe)
        directions = Direction(text=cook_instr, recipe=recipe)
        image = Photo(image=photo)


        ingredients.save()
        directions.save()
        image.save()

        return redirect('/recipes')
    else:
        return render(request, 'create_recipe.html')

#=========================================================================================================


# List views methods


class RecipeListView(ListView):
    model = Recipe
    paginate_by = 100

    def get_queryset(self):
        qs = Recipe.objects.all()
        return qs


class RecipeDetailView(DetailView):
    model = Recipe

    def get_object(self, queryset=None):
        recipe = super(RecipeDetailView, self).get_object(queryset=queryset)
        if 'scale' in self.request.GET:
            recipe.scale = float(self.request.GET['scale'])
            print("set scale to", recipe.scale)
        else:
            recipe.scale = 1.0
        return recipe

