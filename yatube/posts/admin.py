from django.contrib import admin
from .models import Post, Group, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created', 'author')  # Заменили pub_date на created
    list_filter = ('created', 'group')  # Заменили pub_date на created
    search_fields = ('text',)
    empty_value_display = '-пусто-'

admin.site.register(Group)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'created', 'text_short')
    list_filter = ('created', 'author')
    search_fields = ('text', 'author__username', 'post__text')
    
    def text_short(self, obj):
        return obj.text[:50]
    text_short.short_description = 'Текст'