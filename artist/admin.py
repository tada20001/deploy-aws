from django.contrib import admin
from .models import Work


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['id', 'artist', 'title', 'image1', ]
    list_display_links = ['title']
    search_fields = ['title']
    list_select_related = ['artist']
    list_filter = ['category', 'created_at']
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('category')

# @admin.register(Images)
# class ImagesAdmin(admin.ModelAdmin):
#     list_display = ['short_title', 'image']
#     search_fields = ['work']
#     list_filter = ['created_at']
#
#     def short_title(self, images):
#         return images.work.title[:50]
