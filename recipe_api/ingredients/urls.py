from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ingredients import views

app_name = "ingredients"

router = DefaultRouter()
router.register(r"ingredients", views.IngredientViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
