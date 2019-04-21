from django.contrib import admin

# Register your models here.

from .models import Link, SideBar


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'weight', 'created_time']

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)


class SideBarAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_type', 'content', 'status', 'created_time']

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
