from rest_framework import serializers

from recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):


    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_minutes', 'price', 'link'
        ]
        read_only_fields = ['id']


class RecipeDetailSerializer(serializers.ModelSerializer):

    # class Meta:
    #     model = Recipe
    #     fields = [
    #         'id', 'title', 'time_minutes', 'price', 'link', 'description'
    #     ]
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
        