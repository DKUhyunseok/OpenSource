from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('start/', views.start_quiz, name='start'),
    path('submit/', views.submit_quiz, name='submit'),
    path('wrong/', views.wrong_note, name='wrong_note'),

path('add_wrong_note/', views.add_wrong_note, name='add_wrong_note'),
path('remove_wrong/<int:word_id>/', views.remove_wrong_flag, name='remove_wrong'),
path('mode/', views.select_quiz_mode, name='quiz_mode_select'),


]
