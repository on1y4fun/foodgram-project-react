from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Follow, User


class UserAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email', 'bio', 'role',)
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)