from django.shortcuts import render, redirect
from list.models import Word
from .models import QuizResult
from django.contrib.auth.decorators import login_required
import random
from .models import QuizResult, QuizQuestion
from django.shortcuts import get_object_or_404


@login_required
def start_quiz(request):
    mode = request.GET.get('mode', 'text')
    
    # ✅ 오늘의 단어장에 있는 단어만 필터링
    words = list(Word.objects.filter(user=request.user, is_today=True).prefetch_related('meanings'))
    quiz_data = []
    error = None

    # 의미가 없는 단어 제거
    words = [w for w in words if w.meanings.exists()]

    if len(words) < 4:
        error = '오늘의 단어장에서 최소 4개의 단어가 있어야 퀴즈를 시작할 수 있습니다.'
    else:
        # ✅ 오디오 모드일 경우, 오디오 있는 단어만 남김
        if mode == 'audio':
            words = [w for w in words if w.audio_url]

        if len(words) < 4:
            error = '음성 기반 문제를 생성하려면 오디오가 등록된 단어가 최소 4개 이상 필요합니다.'
        else:
            quiz_words = random.sample(words, min(5, len(words)))  # 최대 5문제

            for word in quiz_words:
                # 정답 의미 선택
                meanings = list(word.meanings.all())
                if not meanings:
                    continue
                correct_meaning_obj = random.choice(meanings)
                correct_meaning = correct_meaning_obj.meaning


                # 오답 선택지 만들기 (다른 단어들의 첫 번째 의미 사용)
                other_meanings = [
                    random.choice(list(w.meanings.all())).meaning
                    for w in words if w.id != word.id and w.meanings.exists()
]


                if len(other_meanings) < 3:
                    error = '보기 생성을 위해 최소 4개의 단어가 필요합니다.'
                    break

                choices = random.sample(other_meanings, 3)
                choices.append(correct_meaning)
                random.shuffle(choices)

                quiz_item = {
                    'type': mode,
                    'word_id': word.id,
                    'correct': correct_meaning,
                    'choices': choices,
                }

                if mode == 'text':
                    quiz_item['word'] = word.text
                elif mode == 'audio':
                    quiz_item['audio'] = word.audio_url

                quiz_data.append(quiz_item)

    if not error:
        request.session['quiz_data'] = quiz_data

    return render(request, 'quiz/quiz.html', {
        'quiz_data': quiz_data,
        'error': error,
        'mode': mode
    })



@login_required
def submit_quiz(request):
    quiz_data = request.session.get('quiz_data', [])
    if not quiz_data or request.method != 'POST':
        return redirect('quiz:start')

    correct_count = 0
    result = QuizResult.objects.create(user=request.user, score=0, total=len(quiz_data))

    for i, item in enumerate(quiz_data):
        user_answer = request.POST.get(f'answer_{i}', '').strip()
        correct_answer = item['correct'].strip()

        is_correct = user_answer == correct_answer
        if is_correct:
            correct_count += 1
        else:
            # ✅ 오답일 때 wrong_count 증가
            word_obj = Word.objects.get(id=item['word_id'], user=request.user)
            word_obj.wrong_count += 1
            word_obj.is_wrong = True  # ✅ 이 줄이 있어야 함
            word_obj.save()

        QuizQuestion.objects.create(
            quiz=result,
            word_id=item['word_id'],
            user_answer=user_answer,
            correct_answer=correct_answer,
            is_correct=is_correct,
            choices=item.get('choices', [])
        )

    result.score = correct_count
    result.save()
    del request.session['quiz_data']

    return render(request, 'quiz/result.html', {
        'score': correct_count,
        'total': len(quiz_data),
        'questions': result.questions.all()
    })

from .models import QuizQuestion

@login_required
def wrong_note(request):
    wrong_questions = QuizQuestion.objects.filter(
        quiz__user=request.user,
        is_correct=False,
        word__is_wrong=True
    ).order_by('-quiz__created_at')

    # 중복 제거: 가장 마지막에 틀린 정답만 보여줌
    unique_wrong = {}
    for q in wrong_questions:
        if q.word_id not in unique_wrong:
            unique_wrong[q.word_id] = q

    return render(request, 'quiz/wrong_note.html', {
        'wrong_items': unique_wrong.values()
    })

# quiz/views.py
from list.models import Word  # ✅ Word 모델 불러오기

@login_required
def add_wrong_note(request):
    if request.method == 'POST':
        word_ids = request.POST.getlist('word_ids')
        Word.objects.filter(id__in=word_ids, user=request.user).update(is_wrong=True)
    return redirect('quiz:wrong_note')  # ✅ 오답 노트 페이지로 이동


@login_required
def remove_wrong_flag(request, word_id):
    word = get_object_or_404(Word, id=word_id, user=request.user)
    word.is_wrong = False
    word.save()
    return redirect('quiz:wrong_note')


@login_required
def select_quiz_mode(request):
    return render(request, 'quiz/quiz_mode_select.html')