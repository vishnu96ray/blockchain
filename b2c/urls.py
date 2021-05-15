from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()
admin.site.enable_nav_sidebar = False
from django.conf import settings
from django.conf.urls.static import static
	
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('dprocess.urls')),
    path('', include('business.urls')),


]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)