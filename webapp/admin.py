from django.contrib import admin
from .models import Post, Category, Type, Tag, GlossaryTerm

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Tag)
admin.site.register(GlossaryTerm)