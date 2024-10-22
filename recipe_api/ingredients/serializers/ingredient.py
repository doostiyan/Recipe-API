from rest_framework import serializers

from ingredients.models.ingredient import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name"]
        read_only_fields = ["id"]
