from recipes.views.recipe import BaseRecipeAttrViewSet

from ingredients.models.ingredient import Ingredient
from ingredients.serializers.ingredient import IngredientSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
