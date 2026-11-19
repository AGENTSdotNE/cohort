from rest_framework.routers import SimpleRouter

from .views import InboundItemViewSet

router = SimpleRouter()
router.register('inbound', InboundItemViewSet, basename='inbound-item')

urlpatterns = router.urls
