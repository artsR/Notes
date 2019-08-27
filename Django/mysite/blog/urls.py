from django.conf.urls import url, include
from blog.views import archive

urlpatterns = [
        url(r'^$', archive),
        ]
