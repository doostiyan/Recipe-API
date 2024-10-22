from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tags import views

router = DefaultRouter()
router.register("tags", views.TagViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
