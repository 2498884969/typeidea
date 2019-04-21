from django.contrib import admin

# Register your models here.

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['target', 'content', 'nickname', 'website', 'email', 'status', 'created_time']

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

