from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),       # Home page
    path('blogs/', include('blogs.urls')), # Blogs section
    path('account/', include('account.urls')), # Account section
    path('books/', include('books.urls'))  # Corrected books path
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
