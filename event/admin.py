from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from .models import Event
from markupsafe import Markup, escape

from django.utils.safestring import mark_safe


class EventAdmin(SummernoteModelAdmin):
    list_display = ['id', 'title', 'start_date', 'end_date']
    list_display_links = ['title']
    search_fields = ['title']
    list_filter = ['category', 'created_at']
    list_per_page = 10



admin.site.register(Event, EventAdmin)
