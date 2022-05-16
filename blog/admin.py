from django.contrib import admin
from blog.models import Tag, Post, AuthorProfile



class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

# Register your models here.
admin.site.register(Tag)
admin.site.register(AuthorProfile)
admin.site.register(Post, PostAdmin)