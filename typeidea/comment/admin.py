from django.contrib import admin

# Register your models here.

from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site
from .models import Comment


@admin.register(Comment, site=custom_site)
class CommentAdmin(BaseOwnerAdmin):
    list_display = ['target', 'content', 'nickname', 'website', 'email', 'status', 'created_time']

