from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import QuizResult, QuizQuestion

admin.site.register(QuizResult)
admin.site.register(QuizQuestion)
