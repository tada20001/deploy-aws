from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import Permission
from .filters import UserDateJoinedFilter

from .models import User, Artist, Client, Category, Profile
# Register your models here.

admin.site.register(Permission)


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_artist']
    list_filter = ('is_staff', 'is_active', 'is_client', 'is_artist', 'date_joined', UserDateJoinedFilter)
    search_fields = ['username']
    actions = ['마케팅_이메일보내기']
    list_per_page = 10

    def 마케팅_이메일보내기(self, request, queryset):
        for user in queryset:
            pass
        self.message_user(request, 'hello world')

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_dislay_links = ['user']
    list_select_related = ['user']
    search_fields = ['user']
    list_per_page = 10

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_select_related = ['user']
    list_per_page = 10


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'short_bio', 'website_url']
    list_select_related = ['user']
    search_fields = ['user']
    list_per_page = 10

    def short_bio(self, profile):
        return profile.bio[:20]
