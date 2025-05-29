from django.db import models
from django.contrib.auth.models import User
from list.models import Word  # ✅ 단어장 앱에서 Word 모델 참조

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(QuizResult, on_delete=models.CASCADE, related_name='questions')
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    user_answer = models.TextField()
    correct_answer = models.TextField()
    is_correct = models.BooleanField()
    choices = models.JSONField(blank=True, null=True)  # 객관식 보기 (optional)
