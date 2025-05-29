from django.db import models
from django.contrib.auth.models import User  # 추가

class Word(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    example = models.TextField(blank=True, null=True)
    pronunciation = models.CharField(max_length=100, blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    is_wrong = models.BooleanField(default=False)
    wrong_count = models.IntegerField(default=0)
    is_today = models.BooleanField(default=False)
    today_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.text

class WordMeaning(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='meanings')
    part_of_speech = models.CharField(max_length=50)
    meaning = models.TextField()

    def __str__(self):
        return f"[{self.part_of_speech}] {self.meaning}"



# list/models.py

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)  # 예: business
    display_name = models.CharField(max_length=20)       # 예: 비즈니스

    def __str__(self):
        return self.display_name

class TopicWord(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    meaning = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    part_of_speech = models.CharField(max_length=50, blank=True)  # ✅ 이 줄이 반드시 있어야 함

    def __str__(self):
        return f"[{self.category.display_name}] {self.text}"
