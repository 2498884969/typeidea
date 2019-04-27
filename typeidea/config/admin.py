from django.contrib import admin

# Register your models here.

from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site
from .models import Link, SideBar


@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ['title', 'status', 'weight', 'created_time']


@admin.register(SideBar, site=custom_site)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ['title', 'display_type', 'content', 'status', 'created_time']
