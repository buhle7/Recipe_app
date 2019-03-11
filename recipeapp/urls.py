from django.conf.urls import url

from .views import * #RecipeListView, RecipeDetailView, index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^create/$', create_recipe, name='create'),
    url(r'^details/(?P<id>\d+)/$', recipe_details, name='details'),


    url(r'^$', RecipeListView.as_view(), name="recipe-home"),
    url(r'^list$', RecipeListView.as_view(), name="recipe-list"),
    # recipe detail by slug
    url(r'^recipes/(?P<slug>[-\w]+)/$', RecipeDetailView.as_view(), name="recipe-detail"),
]
