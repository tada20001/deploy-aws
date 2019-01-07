from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect, render
from django.core import serializers
from django.http import Http404, HttpResponse
from artist.models import Work
from django.views.generic import TemplateView

def image_list(request):
    works = Work.objects.all()
    to_json = serializers.serialize('json', works)
    return HttpResponse(to_json, content_type='application/json')


urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('crazyadmin/', admin.site.urls),

    path('summernote/', include('django_summernote.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('ArtandArtists/', include('artist.urls')),
    path('event/', include('event.urls')),

    path('json/', image_list, name='json'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
