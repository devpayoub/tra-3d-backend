from django.contrib import admin
from armodels.models import ARModel

@admin.register(ARModel)
class ARModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'id')
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)
