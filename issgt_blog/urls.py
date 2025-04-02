from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Home page
    path('', include('home.urls')),
    path('blogs/', include('blogs.urls')),  # Blogs section
    path('account/', include('account.urls')),  # Account section
    path('books/', include('books.urls')),  # Corrected books path
    path('', include('contact.urls')),  # For contact
    path('', include('about.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
