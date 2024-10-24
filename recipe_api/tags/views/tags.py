from recipes.views.recipe import BaseRecipeAttrViewSet
from rest_framework.permissions import IsAuthenticated

from tags.models import Tag
from tags.permissions import TagPermission
from tags.serialziers.tags import TagSerializer


class TagViewSet(BaseRecipeAttrViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated, TagPermission)
