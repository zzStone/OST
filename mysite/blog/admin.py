from django.contrib import admin

from blog.models import Post, Blog

class PostAdmin(admin.ModelAdmin):
    search_fields = ["title"]

class BlogAdmin(admin.ModelAdmin):
    search_fields = ["name"]

admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
