from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from armodels.models import ARModel
from armodels.serializers import ARModelSerializer
from drf_spectacular.utils import extend_schema

class ARModelViewSet(viewsets.ModelViewSet):
    serializer_class = ARModelSerializer
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'

    def get_queryset(self):
        """
        B12 Fix: authenticated users only see their own models.
        B3 Fix: retrieve is still public (AllowAny), but queryset is all objects
        so the public share link works regardless of owner.
        """
        if self.action == 'retrieve':
            return ARModel.objects.all().order_by('-created_at')
        if self.request.user and self.request.user.is_authenticated:
            return ARModel.objects.filter(owner=self.request.user).order_by('-created_at')
        return ARModel.objects.none()

    def perform_create(self, serializer):
        """B3 Fix: assign the logged-in user as owner on create."""
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """Allow public access to 'retrieve' action only."""
        if self.action == 'retrieve':
            return [AllowAny()]
        return [IsAuthenticated()]

    @extend_schema(summary="List all 3D models (owned by current user)")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Create a new 3D model")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(summary="Retrieve a 3D model (public)")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary="Update a 3D model")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(summary="Delete a 3D model")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
