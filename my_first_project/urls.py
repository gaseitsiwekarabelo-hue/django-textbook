# my_first_project/urls.py (or myproject/urls.py)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('library.urls', namespace='library')),
    path('', RedirectView.as_view(url='books/', permanent=False)),  # <-- Redirect root to /books/
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)