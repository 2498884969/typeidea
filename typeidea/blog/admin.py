import requests
from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_permission_codename
from django.urls import reverse
from django.utils.html import format_html

from blog.models import Category, Tag, Post
from typeidea import custom_site
from .adminforms import PostAdminForm


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'owner', 'is_nav', 'created_time')
    fields = ('name', 'status', 'owner', 'is_nav')
    list_filter = [CategoryOwnerFilter]
    inlines = [PostInline, ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


PERMISSION_API = 'http://permission.sso.com/has_perm?user={}&perm_code={}'


@admin.register(Post, site=custom_site.custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'category', 'status', 'created_time', 'operator')
    list_display_links = []
    list_filter = ['category']
    search_fields = ['title', 'category__name']
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    # def has_add_permission(self, request):
    #     opts = self.opts
    #     codename = get_permission_codename(action='add', opts=opts)
    #     perm_code = '%s.%s' % (opts.app_label, codename)
    #     resp = requests.get(PERMISSION_API.format(request.user.username, perm_code))
    #     if resp.status_code == 200:
    #         return True
    #     else:
    #         return False
    # fields = (('category', 'title'), 'desc', 'status', 'content', 'tag')

    # def operator(self, obj):
    # return format_html('<a href="{}">编辑</a>', reverse('admin:blog_post_change', args=(obj.id,)))

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>', reverse('cus_admin:blog_post_change', args=(obj.id,)))

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(owner=request.user)

    fieldsets = (('基础配置', {'description': '基础配置描述', 'fields': (('title', 'category'), 'status')}),
                 ('内容', {'fields': ('desc', 'content')}), ('额外信息', {'classes': ('collapse',), 'fields': ('tag',)}))

    filter_vertical = ('tag',)

    # class Media:  #     css = {  #         'all': ('https://cdn.bootcss.com/twitter-bootstrap/4.0.0-beta.2/css/bootstrap.min.css', )  #     }  #     js = ('https://cdn.bootcss.com/twitter-bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)
