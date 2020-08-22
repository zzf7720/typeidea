from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post,Category,Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site



class PostInline(admin.TabularInline):
    fields = ('title','desc')
    extra = 1
    model = Post 



@admin.register(Category,site=custom_site) 
class CategoryAdmin(admin.ModelAdmin):
    # inlines = [PostInline,]
    list_display = ('name','status','is_nav','created_time')
    fields = ('name','status','is_nav')

    def save_model(self,request,obj,form,change):
        obj.owner = request.user
        return super(CategoryAdmin,self).save_model(request,obj,form,change)


@admin.register(Tag,site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')

    def save_model(self,request,obj,form,change):
        obj.owner = request.user
        return super().save_model(request,obj,form,change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户分类 """

    title = '分类过滤'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post,site=custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = [
        'title','category','status',
        'created_time','owner','operator'
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter,]
    search_fields = ['title','category__name']

    exclude = ('owner',)

    # fields = (
    #     ('category','title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('wide',),
            'fields': ('tag', ),
        })
    )
    filter_horizontal = ('tag', )

    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change',args=(obj.id,))
        )   
    operator.short_description = '操作'

    def save_model(self,request,obj,form,change):
        obj.owner = request.user
        return super().save_model(request,obj,form,change)

    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    class Media:
        # css = {
        #     'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
        # }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )
