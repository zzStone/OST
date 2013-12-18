from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
