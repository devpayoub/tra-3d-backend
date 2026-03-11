from django.db import models
from django.conf import settings
import uuid
import os

def model_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    # Use the already-assigned UUID (default=uuid.uuid4 runs before upload)
    # If for any reason id is None, generate a temporary UUID
    model_id = instance.id or uuid.uuid4()
    if ext.lower() == 'glb':
        return f'models/{model_id}/model.{ext}'
    elif ext.lower() == 'usdz':
        return f'models/{model_id}/model.{ext}'
    else:
        return f'models/{model_id}/poster.{ext}'

class ARModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # B3 Fix: track who owns this model to prevent IDOR
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='models',
        null=True,  # null=True for backward compat with existing rows
        blank=True
    )
    name = models.CharField(max_length=255)
    glb_file = models.FileField(upload_to=model_upload_path, null=True, blank=True)
    usdz_file = models.FileField(upload_to=model_upload_path, null=True, blank=True)
    poster = models.ImageField(upload_to=model_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "AR Model"
        verbose_name_plural = "AR Models"

    @property
    def share_url(self):
        from django.conf import settings
        frontend_url = getattr(settings, 'FRONTEND_URL').rstrip('/')
        return f"{frontend_url}/u/{self.id}"

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        # Delete files from S3 when model is deleted
        if self.glb_file:
            self.glb_file.delete(save=False)
        if self.usdz_file:
            self.usdz_file.delete(save=False)
        if self.poster:
            self.poster.delete(save=False)
        super().delete(*args, **kwargs)
