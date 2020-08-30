from django.contrib.sitemaps import views as sitemap_views
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

import xadmin
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from .custom_site import custom_site
from blog.views import IndexView,CategoryView,TagView,PostDetailView,SearchView,AuthorView
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from blog.apis import PostViewSet,CategoryViewSet
from config.views import LinkListView
from comment.views import CommentView
from .autocomplete import CategoryAutocomplete,TagAutocomplete


router = DefaultRouter()
router.register(r'post',PostViewSet,base_name='api-post')
router.register(r'category', CategoryViewSet, base_name='api-category')


urlpatterns = [
    url(r'^$',IndexView.as_view(),name='index'),
    url(r'^links/$',LinkListView.as_view(),name='links'),
    url(r'^comment/$',CommentView.as_view(),name='comment'),
    url(r'^search/$',SearchView.as_view(),name='search'),
    url(r'^author/(?P<owner_id>\d+)/$',AuthorView.as_view(),name='author'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    url(r'^post/(?P<post_id>\d+)$', PostDetailView.as_view(), name='post-detail'),
    url(r'^admin/', xadmin.site.urls, name='xadmin'),
    url(r'^rss|feed/', LatestPostFeed(), name='rss'),
    url(r'^sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}},name='sitemap'),
    url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    url(r'^tag-autocomplete/$', TagAutocomplete.as_view(), name='tag-autocomplete'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^api/',include(router.urls)),
    url(r'^api/docs/', include_docs_urls(title='typeidea apis')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
