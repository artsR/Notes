from django.db import models
from django.contrib import admin

class BlogPost(models.Model):
    title = models.CharField(max_length=150) # why I don't have use 'self.title = ' ?
    body = models.TextField()
    timestamp = models.DateTimeField()
    # additionally Django creates 4th field: auto-incrementing, uniqueID for each
    # model by default.

    class Meta:
        ordering = ('-timestamp',)

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp')



admin.site.register(BlogPost, BlogPostAdmin) # Need to add it to could see my app in admin panel.
