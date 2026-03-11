from django.urls import path, include
from rest_framework.routers import DefaultRouter
from armodels.views import ARModelViewSet

router = DefaultRouter()
router.register(r'models', ARModelViewSet, basename='armodels')

urlpatterns = [
    path('', include(router.urls)),
]
