from django.contrib import admin
from django.urls import path, include
from list import views as list_views

# urls.py (main urls.py)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', list_views.home, name='home'),  # ✅ 메인 페이지
    path('admin/', admin.site.urls),
    path('list/', include('list.urls')),
    path('quiz/', include('quiz.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)