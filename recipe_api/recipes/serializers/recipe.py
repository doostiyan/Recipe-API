from rest_framework import serializers

from recipes.models import Recipe
from tags.models import Tag
from tags.serialziers.tags import TagSerializer


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_minutes', 'price', 'link', 'tags'
        ]
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        for attr,value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class RecipeDetailSerializer(serializers.ModelSerializer):

    # class Meta:
    #     model = Recipe
    #     fields = [
    #         'id', 'title', 'time_minutes', 'price', 'link', 'description'
    #     ]
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
        