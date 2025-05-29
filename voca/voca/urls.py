from django.contrib import admin
from django.urls import path, include
from list import views as list_views

urlpatterns = [
    path('', list_views.home, name='home'),  # ✅ 메인 페이지
    path('admin/', admin.site.urls),
    path('list/', include('list.urls')),
    path('quiz/', include('quiz.urls')),

]
