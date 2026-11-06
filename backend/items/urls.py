from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ItemViewSet

router = DefaultRouter()
router.register("items", ItemViewSet, basename="item")
router.register("categories", CategoryViewSet, basename="category")

urlpatterns = router.urls
