# Voca - 영단어 암기 웹 애플리케이션 사용자 가이드

## 1. 개요

**Voca**는 영어 단어를 검색 및 저장하여 자신만의 단어장을 만들고 주제별 단어, 오늘의 단어장, 퀴즈, 오답 노트를 통해 반복 학습할 수 있는 웹 애플리케이션입니다. 로그인 이후 개인 맞춤형 학습을 제공합니다.

---

## 2. 시작하기

### 회원가입
- 로그인 페이지에서 **회원가입** 버튼 클릭
- `username(이름)`, `비밀번호`, `비밀번호 재입력` 입력 후 가입

### 로그인
- 로그인 화면에서 아이디와 비밀번호 입력
- 로그인 성공 시 단어장 및 학습 기능 이용 가능

### 로그아웃
- 좌측 하단 **로그아웃** 버튼 클릭 → 로그인 화면으로 이동

### 관리자(admin)
- 회원 정보 관리 (이름, 아이디, 이메일, 관리자 여부)
- 비밀번호는 알고리즘으로 암호화되어 저장
- 참여 날짜, 마지막 로그인 날짜, 유저 그룹, 권한 등 관리 가능

---

## 3. 단어 검색 & 저장

- 상단 메뉴에서 **단어 검색** 클릭
- 검색어 입력 → 사전 API로부터 뜻, 품사, 예문, 발음(mp3) 표시
- **단어장에 추가** 버튼 클릭 시 내 단어장에 저장
  - 이미 존재하는 단어는 중복 알림 표시

---

## 4. 내 단어장 관리

### 단어장 보기
- **단어 노트** 메뉴에서 저장한 단어를 최신순으로 확인 가능

### 단어 상세 보기
- 단어 카드의 `+` 버튼 클릭 시 상세 정보 모달 열림

### 단어 삭제
- 단어 카드의 **휴지통 아이콘** 클릭

### 직접 추가
- `+ 직접 추가` 버튼 클릭 → 단어, 뜻, 품사 직접 입력하여 저장
  - API 연결이 안될 경우 유용

---

## 5. 오늘의 단어장

### 추가하기
- 오늘의 단어장이 비어 있으면 **편집하기** 화면으로 이동

### 편집하기
- 기존 보유 단어 중 선택하여 오늘 학습할 단어로 저장

- 오늘의 단어는 **퀴즈 대상**

---

## 6. 퀴즈 기능

### 퀴즈 모드 선택
- **퀴즈 시작** 클릭 후 `텍스트` 또는 `오디오` 모드 선택

### 문제 풀이
- **텍스트 기반**: 영어 단어 → 한글 뜻 4지선다형 객관식
- **오디오 기반**: 발음 듣기 → 한글 뜻 4지선다형 객관식

### 결과 및 오답노트
- 퀴즈 결과: 점수 및 정·오답 리스트 표시
- 틀린 단어는 자동으로 **오답 노트**에 등록 가능

### 오답 노트
- 오답 단어만 모아서 복습 가능
- 학습 완료 시 **플래그 해제**

---

## 7. 주제별 단어 학습

- 토익 등 시험에 자주 출제되는 단어를 **주제별**로 제공
- 각 단어는 의미와 품사를 함께 제공

### 학습 흐름
1. `주제별` 카테고리 선택
2. 단어 리스트 확인 및 암기
3. 모르는 단어는 바로 **검색 버튼**으로 사전 검색 → 단어장에 쉽게 추가

- 본인이 입력한 뜻·품사와 정답 비교를 통해 **자가 진단** 가능

### 관리자(admin 기능)
- 카테고리(주제) 등록, 수정, 삭제 가능
- 카테고리에 단어를 직접 추가하거나 **CSV 업로드**로 대량 등록 가능

---






# Developer's Guide (개발자 가이드)

## 1. 기술 스택

- **Backend**: Python, Django  
- **Database**: SQLite, PostgreSQL  
- **Frontend**: Django Templates + CSS / HTMX (모달 기반 인터페이스)  
- **External APIs**:  
  - DictionaryAPI – 단어 사전 검색 데이터  
  - DeepL API – 뜻 번역, 예문 번역  
  - ElevenLabs TTS – 단어 오디오(mp3) 생성  

---

## 2. 설정 방법

### 1) 클론 & 가상환경 설정

```bash
$ git clone https://github.com/DKUhyunseok/OpenSource.git
$ cd OpenSource
$ cd voca
```

### 2) 의존성 설치

Django 백엔드 의존성 설치:

```bash
$ pip install -r requirements.txt
```

### 3) 환경 변수 설정

`.env` 파일 또는 `settings.py`에 아래와 같이 외부 API 키를 등록해야 합니다:

- `elevenlabs API`: 개인 키 필요 (부분 무료/유료)
- `deepl API`: 개인 키 필요 (부분 무료/유료)
- `freedictionary API`: 무료 사용 가능

### 4) 개발 서버 실행

Django 서버 실행:

```bash
$ python manage.py runserver
```

로컬 주소: http://127.0.0.1:8000



## 3. OpenSource-main 디렉토리 구조

```
OpenSource-main/
├── voca/
│   ├── db.sqlite3                    # SQLite DB 파일 (단어 및 사용자 데이터 저장)
│   ├── manage.py                     # Django 프로젝트 관리 명령어 진입점
│   ├── list/                         # 메인 앱 디렉토리
│   │   ├── admin.py                  # 관리자 페이지 설정
│   │   ├── apps.py                   # 앱 구성 정보 정의
│   │   ├── context_processors.py     # 템플릿 공용 데이터 주입 처리
│   │   ├── forms.py                  # 단어 입력 및 수정용 폼 정의
│   │   ├── models.py                 # Word, WordMeaning, Category 등 모델 정의
│   │   ├── urls.py                   # URL 라우팅 정보 정의
│   │   ├── views.py                  # 단어 노트, 시험, 오답 노트 등 기능 구현 뷰
│   │   ├── migrations/              # DB 마이그레이션 히스토리 저장 폴더
│   │   │   ├── 0001_initial.py       # 초기 모델 마이그레이션
│   │   │   ├── ...                   # 이후 모델 변경 사항들
│   │   │   └── 0011_word_translated_example.py
│   │   └── __pycache__/             # 마이그레이션 캐시 파일
│   ├── static/
│   │   └── list/
│   │       ├── css/
│   │       │   └── style.css        # 전체 프론트 스타일 정의
│   │       ├── img/
│   │       │   └── search.svg       # 아이콘 및 정적 이미지
│   │       └── js/
│   │           ├── word_note.js     # 단어 노트 관련 자바스크립트
│   │           └── word_quiz.js     # 단어 시험 관련 자바스크립트
│   └── templates/
│       └── list/
│           ├── word_note.html       # 단어 노트 템플릿
│           ├── word_quiz.html       # 퀴즈 문제 화면
│           ├── quiz_result.html     # 퀴즈 결과 출력 화면
│           └── wrong_note.html      # 오답 노트 출력 화면
```


# Django 모델 정의

## Word 모델

| 필드명              | 타입                  | 설명                 |
|---------------------|-----------------------|----------------------|
| user                | ForeignKey(User)      | 단어 등록 유저       |
| text                | CharField(100)        | 단어 본문            |
| example             | TextField             | 예문                 |
| pronunciation       | CharField(100)        | 발음                 |
| audio_url           | URLField              | TTS 오디오 링크       |
| audio_file          | FileField             | 업로드된 오디오 파일 |
| added_at            | DateTimeField         | 등록일               |
| is_wrong            | BooleanField          | 오답 여부            |
| wrong_count         | IntegerField          | 오답 횟수            |
| is_today            | BooleanField          | 오늘의 단어 여부     |
| today_date          | DateField             | 오늘 날짜            |
| translated_example  | TextField             | 예문 번역            |

---

## WordMeaning 모델

| 필드명         | 타입               | 설명       |
|----------------|--------------------|------------|
| word           | ForeignKey(Word)   | 연결된 단어 |
| part_of_speech | CharField(50)      | 품사       |
| meaning        | TextField          | 뜻         |

---

## Category 모델

| 필드명       | 타입             | 설명        |
|--------------|------------------|-------------|
| name         | CharField(20)    | 내부 명칭   |
| display_name | CharField(20)    | 사용자용 명칭 |

---

## TopicWord 모델

| 필드명         | 타입                 | 설명          |
|----------------|----------------------|---------------|
| category       | ForeignKey(Category) | 연결 카테고리 |
| text           | CharField(100)       | 단어          |
| meaning        | TextField            | 뜻            |
| created_at     | DateTimeField        | 생성일시      |
| part_of_speech | CharField(50)        | 품사          |

# 4. 주요 함수

voca 프로젝트 내 Django View / 유틸 함수  
함수 핵심 동작을 요약
---

## `list/views.py`

### `word_detail(request, word_id)`
단어 상세 페이지(또는 모달)를 렌더링합니다. `word_id`로 사용자 소유 **Word** 인스턴스를 조회하고 품사·뜻(`WordMeaning`)과 발음·예문을 포함해 템플릿 `word_detail.html`(또는 모달 partial)에 전달합니다. 없는 경우 404 또는 redirect.

### `wordbook(request)`
사용자 단어장(Word Note) 메인 화면을 보여줍니다. 로그인 사용자의 `Word`를 최신 저장 순으로 페이지네이션하여 `word_note.html` 템플릿에 전달합니다.

### `delete_word(request, word_id)`
Word 인스턴스를 삭제합니다. **POST** 요청만 허용하며, 성공 시 단어장 목록으로 redirect.

### `today_wordbook(request)`
`is_today=True` 로 필터링된 단어만 보여주는 **오늘의 단어장** 페이지를 렌더링합니다. 비어 있으면 편집 화면 안내.

### `edit_today_wordbook(request)`
오늘 학습할 단어를 선택·저장하는 편집 폼 처리. **POST** 요청에서 체크된 `word_ids`를 받아 `is_today` 플래그 갱신 후 `today_wordbook`으로 redirect.

### `word_detail_modal(request, word_id)`
AJAX 전용: 단어 카드의 ‘+’ 버튼 클릭 시 비동기 요청으로 단어 상세 HTML 조각 반환.

### `manual_add_word(request)`
API 실패 시 수동으로 단어·뜻·품사를 입력해 Word 저장. **GET**: 폼, **POST**: 저장.

### `list_index(request)`
‘단어 목록(Home)’ 대시보드. 검색, 단어장 바로가기 카드 등을 종합적으로 표시.

### `search_word(request)`
검색어를 외부 사전 API로 조회해 결과를 JSON 또는 HTML로 반환. 필요 시 `generate_tts_and_save` · `translate_to_korean` 호출.

### `add_to_wordbook(request)`
검색 결과에서 ‘단어장에 추가’ 클릭 시 Word 저장. 이미 존재하면 JSON으로 ‘중복’ 메시지.

### `topic_quiz(request, category)`
선택한 **Category**의 `TopicWord`로 즉시 퀴즈를 생성·출제.

---

### `home(request)`
Landing 페이지. 로그인 여부에 따라 리다이렉트 또는 소개 페이지 렌더.

### `logout_view(request)`
Django `logout()` 호출 후 로그인 페이지로 redirect.

---

### `signup_view(request)`
회원가입 폼 표시·처리. 성공 시 로그인 페이지로 redirect.

### `signup_modal(request)`
모달 기반 회원가입(AJAX). POST 시 JSON 응답.

### `login_view(request)`
로그인 폼 표시·처리. 성공 시 `next` 파라미터 또는 홈으로 redirect.

---

### `generate_tts_and_save(word_obj)`
외부 TTS API 호출로 음성 파일(mp3)을 생성 후 `word_obj.audio_url`에 저장. 이미 파일이 있으면 건너뜀.

### `translate_to_korean(text)`
DeepL·Papago API를 사용해 영어 예문을 한국어로 번역.


## `quiz/views.py`

### `start_quiz(request)`
* **설명**  
로그인 사용자의 *오늘의 단어장*(`Word.is_today=True`) 로드  
(audio 모드) `audio_url`이 없는 단어 제외  
단어 개수 < 4 ⇒ 오류 메시지 반환  
최대 5개 단어를 무작위 선정, 각 단어의 의미를 정답으로 삼고 나머지 단어의 의미로 오답 보기(4지선다) 구성  
문제 리스트를 `request.session['quiz_data']`에 저장 후 `quiz/quiz.html` 렌더  

---

### `submit_quiz(request)`
* **설명**  
세션에 저장된 `quiz_data`가 없으면 `/quiz/start/`로 리다이렉트  
`QuizResult` 레코드 생성 (score = 0)  
각 문제에 대해 사용자의 답(`answer_i`)과 정답 비교  
* 정답 → `correct_count ++`  
* 오답 → 해당 Word의 `wrong_count ++`, `is_wrong=True` 설정  
* `QuizQuestion` 레코드에 선택지·정오답 저장  
최종 점수를 `QuizResult.score`에 기록, 세션 `quiz_data` 삭제  
`quiz/result.html` 렌더 (`score`, `total`, `questions` 전달)  

---

### `wrong_note(request)`
* **설명**  
  * 사용자가 최근 틀린 단어를 `QuizQuestion` → `is_correct=False`, `Word.is_wrong=True` 조건으로 조회  
  * 단어 ID별로 가장 최근 오답만 남겨 중복 제거  
  * `quiz/wrong_note.html` 템플릿에 `wrong_items` 컨텍스트 전달  

---

### `add_wrong_note(request)`  
* **설명**  
  * 요청 폼의 `word_ids` 리스트를 받아 해당 Word 레코드의 `is_wrong=True`로 일괄 업데이트  
  * 완료 후 오답 노트 페이지(`quiz:wrong_note`)로 리다이렉트  

---

### `remove_wrong_flag(request, word_id)`
* **설명**  
  * 지정 Word를 조회(`get_object_or_404`) 후 `is_wrong=False`로 변경  
  * 오답 노트 페이지로 리다이렉트  

---

### `select_quiz_mode(request)`
* **설명**  
  * 텍스트/오디오 중 퀴즈 모드 선택 화면(`quiz/quiz_mode_select.html`) 렌더  

---


# 5. 개선·확장 제안

| 영역 | 제안 내용 | 기대 효과 |
|------|-----------|-----------|
| **보안** | • 비밀번호 재설정 이메일<br>• `django‑axes` Brute‑force 방지<br>• CSRF 쿠키 | 계정 도용·무차별 대입 공격 예방 |
| **UX / UI** | • 오프라인 퀴즈<br>• 다크 모드| 반응형·모바일 경험 향상 |
| **성능** | • Redis 캐시 + Celery 비동기 TTS <br>• DB 쿼리 프로파일링 & 인덱스 최적화 | 페이지 로드·API 응답 지연 최소화 |
| **배포** | • Dockerfile + docker‑compose | 배포 일관성·스케일 아웃 용이 |
| **데이터 분석** | • 학습 진척도 Dash (사용자별 퀴즈 정확도 차트)| 개인화 학습 효과 극대화 |
| **알림** | • Email / WebPush 알림: “오늘의 단어 퀴즈 시간” | 사용자 경험 상승 |
| **접근성** | • 키보드 내비게이션<br>• 오디오 컨트롤 키보드 단축키 | A11y 적합성 확보 |

