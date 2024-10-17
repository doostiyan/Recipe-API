from rest_framework.routers import DefaultRouter

from recipes import views

app_name = 'recipes'
router = DefaultRouter()

router.register(r'recipes', views.RecipeViewSet, basename='recipe')