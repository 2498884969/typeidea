from django.contrib import admin

# Register your models here.
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html

from blog.models import Category, Tag, Post
from typeidea import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from .adminforms import PostAdminForm


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site.custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time')
    fields = ('name', 'status', 'owner', 'is_nav')
    inlines = [PostInline, ]

    def post_count(self, obj):
        return obj.post_set.count

    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site.custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site.custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ('title', 'category', 'status', 'created_time', 'operator')
    list_display_links = []
    list_filter = [CategoryOwnerFilter, ]
    search_fields = ['title', 'category__name']
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    fieldsets = (('基础配置', {'description': '基础配置描述', 'fields': (('title', 'category'), 'status')}),
                 ('内容', {'fields': ('desc', 'content')}),
                 ('额外信息', {'classes': ('collapse',), 'fields': ('tag',)}))

    filter_vertical = ('tag',)

    # 操作
    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>', reverse('cus_admin:blog_post_change', args=(obj.id,)))

    operator.short_description = '操作'


@admin.register(LogEntry, site=custom_site.custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    """操作日志"""

    list_display = ['object_repr', 'object_id', 'action_flag', 'action_flag',
                    'user', 'change_message']


