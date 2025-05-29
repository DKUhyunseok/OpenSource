import requests
from django.shortcuts import render, redirect
from .models import Word
from .forms import SearchForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Word
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

import os
import requests
from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from .models import Word


def generate_tts_and_save(word_obj):
    """
    ElevenLabs TTS API를 통해 단어의 오디오를 생성하고 저장한 후,
    word.audio_url에 경로를 저장합니다.
    """
    if word_obj.audio_url and word_obj.audio_url.strip() != "":
        return  # 오디오가 이미 있으면 skip

    API_KEY = 'sk_25873f760bb4695cc39ccecd4afd01a20713f79ba43d4cab'
    VOICE_ID = 'EXAVITQu4vr4xnSDxMaL'  # 기본 남성 영어 음성 ID
    headers = {
        'xi-api-key': API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        "text": word_obj.text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        folder = os.path.join(settings.MEDIA_ROOT, 'audio')
        os.makedirs(folder, exist_ok=True)
        filename = f"{word_obj.text}.mp3"
        file_path = os.path.join(folder, filename)

        with open(file_path, 'wb') as f:
            f.write(response.content)

        word_obj.audio_url = f"audio/{filename}"
        word_obj.save()
    else:
        print("TTS API 호출 실패:", response.status_code, response.text)




def translate_to_korean(text):
    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "auth_key": "f94cbcc9-6485-4d73-8d18-307e1e872729:fx",  # <-- 여기에 실제 키 입력
        "text": text,
        "target_lang": "KO"
    }
    response = requests.post(url, data=data, headers=headers)
    result = response.json()
    return result["translations"][0]["text"]


def home(request):
    if request.user.is_authenticated:
        return redirect('wordbook')

    login_form = AuthenticationForm(request, data=request.POST or None)
    signup_form = UserCreationForm()

    # ✅ 로그인 시도일 때만
    if request.method == 'POST' and 'username' in request.POST and 'password' in request.POST:
        if login_form.is_valid():
            login(request, login_form.get_user())
            return redirect( 'wordbook')

    return render(request, 'list/home.html', {
        'form': login_form,
        'signup_form': signup_form
    })


def logout_view(request):
    logout(request)
    return redirect('home')  # 로그아웃 시 홈으로

def list_index(request):
    return redirect('search')  # name='search'는 urls.py에 정의된 것 기준

def search_word(request):
    query = request.GET.get('q')
    result = None
    alert_word = request.session.pop('word_duplicate', None)

    if query:
        api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{query}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                entry = data[0]
                word = entry.get('word', '')
                meanings = []

                for meaning in entry.get('meanings', []):
                    part_of_speech = meaning.get('partOfSpeech', '')
                    definitions = []

                    for d in meaning.get('definitions', [])[:5]:
                        eng_def = d['definition'].strip()
                        if not eng_def:
                            continue
                        try:
                            kor_def = translate_to_korean(eng_def)
                        except Exception:
                            kor_def = eng_def  # 번역 실패 시 원문 사용
                        definitions.append(kor_def)

                    meanings.append({
                        'part_of_speech': part_of_speech,
                        'definitions': definitions
                    })

                # 예문 처리 + 번역
                example = ''
                translated_example = ''
                if entry.get('meanings') and entry['meanings'][0].get('definitions'):
                    example = entry['meanings'][0]['definitions'][0].get('example', '')
                    if example:
                        try:
                            translated_example = translate_to_korean(example)
                        except Exception:
                            translated_example = ''

                # 발음 및 오디오 처리
                pronunciation = ''
                audio = ''
                if 'phonetics' in entry and entry['phonetics']:
                    pronunciation = entry['phonetics'][0].get('text', '')
                    audio = entry['phonetics'][0].get('audio', '')

                # 오디오가 없으면 → TTS로 생성
                if not audio:
                    class TempWord:
                        def __init__(self, text):
                            self.text = text
                            self.audio_url = ''
                        def save(self): pass

                    temp_word = TempWord(word)
                    generate_tts_and_save(temp_word)
                    if temp_word.audio_url:
                        audio = f"/media/{temp_word.audio_url}"

                result = {
                    'word': word,
                    'meanings': meanings,
                    'example': example,
                    'translated_example': translated_example,
                    'pronunciation': pronunciation,
                    'audio': audio,
                }

    return render(request, 'list/search.html', {
        'result': result,
        'query': query,
        'alert_word': alert_word,
    })




from .models import WordMeaning

@login_required
def add_to_wordbook(request):
    if request.method == 'POST':
        raw_word = request.POST['word']
        example = request.POST.get('example', '')
        translated_example = request.POST.get('translated_example', '')
        pronunciation = request.POST.get('pronunciation', '')
        audio_url = request.POST.get('audio', '')
        meanings_json = request.POST.get('meanings_json', '[]')

        import json
        meaning_items = json.loads(meanings_json)

        normalized_word = raw_word.strip().lower()
        is_duplicate = Word.objects.filter(user=request.user, text=normalized_word).exists()

        if is_duplicate:
            request.session['word_duplicate'] = raw_word
        else:
            word = Word.objects.create(
                user=request.user,
                text=normalized_word,
                example=example,
                translated_example=translated_example,
                pronunciation=pronunciation,
            )

            for item in meaning_items:
                WordMeaning.objects.create(
                    word=word,
                    part_of_speech=item.get('part_of_speech', ''),
                    meaning=item.get('definition', '')
                )

            if audio_url.strip():
                word.audio_url = audio_url.strip()
                word.save()
            else:
                generate_tts_and_save(word)  # 이 함수 안에서 word.save() 처리됨

        return redirect('search')

    return redirect('search')


@login_required
def word_detail(request, word_id):
    word = get_object_or_404(Word, id=word_id, user=request.user)
    return render(request, 'list/word_detail.html', {'word': word})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'list/signup.html', {'form': form})


from .forms import SignupForm
def signup_modal(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('wordbook')
        else:
            login_form = AuthenticationForm()
            return render(request, 'list/home.html', {
                'form': login_form,
                'signup_form': form,
                'show_modal': True  # ✅ 오직 회원가입 실패 시만 모달 뜸
            })
    return redirect('home')



@login_required
def wordbook(request):
    words = Word.objects.filter(user=request.user).order_by('-added_at')  # ✅ 본인만
    return render(request, 'list/wordbook.html', {'words': words})

from django.contrib.auth import logout


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # ✅ 로그인 후 원래 페이지로 이동
            next_url = request.GET.get('next') or 'wordbook'
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'list/login.html', {'form': form})



@login_required
def delete_word(request, word_id):
    word = get_object_or_404(Word, id=word_id, user=request.user)
    word.delete()
    return redirect('wordbook')



from django.shortcuts import render, get_object_or_404
from .models import TopicWord, Category

def topic_words(request, category):
    category_obj = Category.objects.filter(name=category).first()

    if not category_obj:
        return render(request, 'list/topic_not_found.html', {'category': category})

    topics = TopicWord.objects.filter(category=category_obj)
    categories = Category.objects.all()

    return render(request, 'list/topic_words.html', {
        'topics': topics,
        'categories': categories,
        'category': category,
    })



from datetime import date
from django.views.decorators.http import require_POST

@login_required
def today_wordbook(request):
    words = Word.objects.filter(user=request.user, is_today=True)
    return render(request, 'list/today_wordbook.html', {'words': words})


from django.views.decorators.http import require_http_methods
from .models import Word

@require_http_methods(["GET", "POST"])
@login_required
def edit_today_wordbook(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist('word_ids')
        Word.objects.filter(user=request.user).update(is_today=False)
        Word.objects.filter(user=request.user, id__in=selected_ids).update(is_today=True)
        return redirect('today_wordbook')

    # 오답순 포함 + 최신순 정렬
    words = Word.objects.filter(user=request.user).order_by('-added_at')
    return render(request, 'list/edit_today_wordbook.html', {'words': words})



from django.shortcuts import render, redirect, get_object_or_404
from .models import TopicWord, Category

def topic_quiz(request, category):
    category_obj = get_object_or_404(Category, name=category)
    words = TopicWord.objects.filter(category=category_obj)

    if request.method == "POST":
        results = []
        for word in words:
            user_pos = request.POST.get(f'pos_{word.id}', '').strip()
            user_meaning = request.POST.get(f'meaning_{word.id}', '').strip()
            results.append({
                'text': word.text,  # ✅ 단어만 저장
                'correct_pos': word.part_of_speech,
                'correct_meaning': word.meaning,
                'user_pos': user_pos,
                'user_meaning': user_meaning,
})

        return render(request, 'list/topic_quiz_result.html', {
            'category': category,
            'results': results,
        })

    return render(request, 'list/topic_quiz.html', {
        'category': category,
        'words': words,
    })

from django.template.loader import render_to_string
from django.http import JsonResponse

@login_required
def word_detail_modal(request, word_id):
    word = get_object_or_404(Word, id=word_id, user=request.user)
    html = render_to_string('list/word_detail.html', {'word': word}, request=request)
    return JsonResponse({'html': html})



@login_required
def manual_add_word(request):
    if request.method == 'POST':
        word_text = request.POST.get('word', '').strip().lower()
        meaning_text = request.POST.get('meaning', '').strip()
        example = request.POST.get('example', '').strip()
        translated_example = request.POST.get('translated_example', '').strip()
        pronunciation = request.POST.get('pronunciation', '').strip()

        if not word_text or not meaning_text:
            return HttpResponse("<script>alert('단어와 뜻은 필수입니다.');history.back();</script>")

        if Word.objects.filter(user=request.user, text=word_text).exists():
            return HttpResponse(f"<script>alert('이미 \"{word_text}\" 단어가 등록되어 있습니다.');history.back();</script>")

        word = Word.objects.create(
            user=request.user,
            text=word_text,
            example=example,
            translated_example=translated_example,  # ✅ 추가
            pronunciation=pronunciation,
        )
        WordMeaning.objects.create(
            word=word,
            part_of_speech='manual',
            meaning=meaning_text
        )

        generate_tts_and_save(word)

        return redirect('wordbook')

    return render(request, 'list/manual_add.html')
