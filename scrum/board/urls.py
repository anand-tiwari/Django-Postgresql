from rest_framework.routers import DefaultRouter

from board import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
