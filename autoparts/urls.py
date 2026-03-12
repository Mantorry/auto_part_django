from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('catalog.urls')),
    path('account/', include('account.urls')),
    path('receipt/', include('receipt.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('admin-panel/', include('panel.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
