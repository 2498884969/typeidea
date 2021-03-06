"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from .custom_site import custom_site
from blog.views import PostDetailView, TagView, IndexView, CategoryView
from config.views import links

"""
1. 博客首页：/
2. 博文详情页:/post/<post_id>.html
3. 分类列表页：/category/<category_id>/
4. 标签列表页：/tag/<tag_id>/
5. 友链展示页：/links/

reverse: 通过name反向解析出URL
"""

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^super_admin/', custom_site.urls, name='super-admin'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post-detail'),
    url(r'^links/$', links, name='links')

]
