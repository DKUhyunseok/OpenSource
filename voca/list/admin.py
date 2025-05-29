from django.contrib import admin
from .models import TopicWord, Category
import csv
from io import TextIOWrapper
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path
from django.template.response import TemplateResponse

@admin.register(TopicWord)
class TopicWordAdmin(admin.ModelAdmin):
    list_display = ['category', 'text', 'meaning', 'part_of_speech']
    change_list_template = "admin/list/topicword/change_list.html"

    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST' and 'csv_file' in request.FILES:
            file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
            reader = csv.DictReader(file)

            count = 0
            for row in reader:
                # 카테고리 가져오거나 생성
                category_obj, _ = Category.objects.get_or_create(
                    name=row['category'],
                    defaults={'display_name': row['category']}
                )

                # 단어 등록 또는 업데이트 (루프 내부에 위치해야 함)
                _, created = TopicWord.objects.update_or_create(
                    category=category_obj,
                    text=row['text'],
                    defaults={
                        'meaning': row['meaning'],
                        'part_of_speech': row.get('part_of_speech', ''),
                    }
                )

                if created:
                    count += 1

            self.message_user(request, f"{count}개의 단어가 업로드되었습니다.", level=messages.SUCCESS)
            return redirect(request.path)

        extra_context = extra_context or {}
        extra_context['csv_upload_form'] = True
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_name']
