from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_word, name='search'),
    path('add/', views.add_to_wordbook, name='add'),
    path('wordbook/', views.wordbook, name='wordbook'),
    path('login/', views.login_view, name='login'),         # ✅ 로그인
    path('logout/', views.logout_view, name='logout'),       # ✅ 로그아웃
    path('signup/', views.signup_view, name='signup'),       # ✅ 회원가입
    path('', views.home, name='home'),
    path('delete/<int:word_id>/', views.delete_word, name='delete_word'),
    path('word/<int:word_id>/', views.word_detail, name='word_detail'),
    path('signup_modal/', views.signup_modal, name='signup_modal'),
    path('topic/<str:category>/', views.topic_words, name='topic_words'),
    path('wordbook/today/', views.today_wordbook, name='today_wordbook'),
    path('wordbook/today/edit/', views.edit_today_wordbook, name='edit_today_wordbook'),
    path('word/<int:word_id>/', views.word_detail, name='word_detail'),
    path('wordbook/add/', views.manual_add_word, name='manual_add_word'),


    path('topic/<str:category>/quiz/', views.topic_quiz, name='topic_quiz'),

]