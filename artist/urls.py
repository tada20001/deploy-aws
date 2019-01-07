from django.urls import path, register_converter
from . import views
from .converters import SlugUnicodeConverter

register_converter(SlugUnicodeConverter, 'myslug')

app_name = 'ArtandArtists'

urlpatterns = [
    # path('artist_list/', views.artist_list, name='artist_list'),
    path('artists/<int:artist_id>/', views.artist_detail, name='artist_detail'),
    path('category/<myslug:category>/', views.works_by_category, name='works_by_category'),

    path('', views.work_list, name='work_list'),
    path('<int:id>/', views.work_detail, name='work_detail'),
    path('<int:id>/edit/', views.work_edit, name='work_edit'),
    path('create/', views.work_create, name='work_create'),
    path('<int:pk>/delete/', views.work_delete, name='work_delete'),

    path('like_work/', views.like_work, name='like_work'),

    path('about/', views.about_us, name='about_us'),
]
