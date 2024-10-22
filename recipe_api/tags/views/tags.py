from recipes.views.recipe import BaseRecipeAttrViewSet

from tags.models import Tag
from tags.serialziers.tags import TagSerializer


class TagViewSet(BaseRecipeAttrViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
