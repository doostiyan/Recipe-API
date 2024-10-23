from recipes.views.recipe import BaseRecipeAttrViewSet
from rest_framework.permissions import IsAuthenticated

from ingredients.models.ingredient import Ingredient
from ingredients.permissions import IngredientPermission
from ingredients.serializers.ingredient import IngredientSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticated, IngredientPermission)
