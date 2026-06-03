import json
import base64
import requests
from config import (
    ANKI_CONNECT_URL, DECK_NAME, MODEL_NAME,
    CARD_FRONT_TEMPLATE, CARD_BACK_TEMPLATE, CARD_CSS,
    SENTENCE_MODEL_NAME, SENTENCE_DECK_NAME,
    SENTENCE_FRONT_TEMPLATE, SENTENCE_BACK_TEMPLATE, SENTENCE_CSS,
)


def _invoke(action, **params):
    payload = {"action": action, "version": 6, "params": params}
    try:
        resp = requests.post(ANKI_CONNECT_URL, json=payload, timeout=5)
        resp.raise_for_status()
        result = resp.json()
    except requests.ConnectionError:
        raise ConnectionError(
            "无法连接 AnkiConnect，请确认：\n"
            "  1. Anki 桌面版正在运行\n"
            "  2. 已安装 AnkiConnect 插件（代码：2055492159）"
        )
    except requests.RequestException as e:
        raise RuntimeError(f"AnkiConnect 请求失败: {e}")

    if result.get("error"):
        raise RuntimeError(f"AnkiConnect 错误: {result['error']}")
    return result.get("result")


def ensure_deck(deck_name=None):
    _invoke("createDeck", deck=deck_name or DECK_NAME)


def ensure_model():
    models = _invoke("modelNames")
    if MODEL_NAME in models:
        # 确保 Audio 字段存在（兼容旧版模型）
        fields = _invoke("modelFieldNames", modelName=MODEL_NAME)
        if "Audio" not in fields:
            _invoke("modelFieldAdd", modelName=MODEL_NAME, fieldName="Audio", index=5)
            # 更新卡片模板加入发音
            _invoke("updateModelTemplates", model={
                "name": MODEL_NAME,
                "templates": {
                    "Card 1": {
                        "Front": CARD_FRONT_TEMPLATE,
                        "Back": CARD_BACK_TEMPLATE,
                    }
                }
            })
        return

    _invoke(
        "createModel",
        modelName=MODEL_NAME,
        inOrderFields=["Word", "Phonetic", "Definition", "Example", "Note", "Audio"],
        css=CARD_CSS,
        cardTemplates=[
            {
                "Name": "Card 1",
                "Front": CARD_FRONT_TEMPLATE,
                "Back": CARD_BACK_TEMPLATE,
            }
        ],
    )


def get_deck_names():
    return _invoke("deckNames")


def check_duplicate(word, deck_name=None):
    deck = deck_name or DECK_NAME
    result = _invoke("findNotes", query=f'"deck:{deck}" "Word:{word}"')
    return len(result) > 0 if result else False


def download_audio(word):
    """下载有道发音并通过 AnkiConnect 存入 Anki media"""
    filename = f"youdao_{word}.mp3"
    url = f"https://dict.youdao.com/dictvoice?audio={word}&type=2"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        audio_b64 = base64.b64encode(resp.content).decode("utf-8")
        _invoke("storeMediaFile", filename=filename, data=audio_b64)
        return f"[sound:{filename}]"
    except Exception:
        return ""


def add_note(word, phonetic, definition, example, note="", deck_name=None):
    deck = deck_name or DECK_NAME
    ensure_deck(deck)
    ensure_model()

    if check_duplicate(word, deck):
        return False, "该单词已存在于牌组中"

    audio = download_audio(word)

    note_id = _invoke(
        "addNote",
        note={
            "deckName": deck,
            "modelName": MODEL_NAME,
            "fields": {
                "Word": word,
                "Phonetic": phonetic,
                "Definition": definition,
                "Example": example,
                "Note": note,
                "Audio": audio,
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": deck,
                    "checkChildren": False,
                },
            },
        },
    )
    return True, note_id


def ensure_sentence_model():
    models = _invoke("modelNames")
    if SENTENCE_MODEL_NAME in models:
        # 确保模板是最新的
        _invoke("updateModelTemplates", model={
            "name": SENTENCE_MODEL_NAME,
            "templates": {
                "Card 1": {
                    "Front": SENTENCE_FRONT_TEMPLATE,
                    "Back": SENTENCE_BACK_TEMPLATE,
                }
            }
        })
        return

    _invoke(
        "createModel",
        modelName=SENTENCE_MODEL_NAME,
        inOrderFields=["Chinese", "English", "Grammar", "Note", "Audio"],
        css=SENTENCE_CSS,
        cardTemplates=[
            {
                "Name": "Card 1",
                "Front": SENTENCE_FRONT_TEMPLATE,
                "Back": SENTENCE_BACK_TEMPLATE,
            }
        ],
    )


def download_sentence_audio(english):
    """下载整句英文发音（通过有道翻译 API 获取 TTS URL）"""
    import hashlib
    clean = english.strip().replace("\n", " ").replace("\r", "")
    name_hash = hashlib.md5(clean.encode()).hexdigest()[:10]
    filename = f"sentence_{name_hash}.mp3"

    try:
        # 通过翻译接口获取英文发音 URL
        resp = requests.post(
            "https://aidemo.youdao.com/trans",
            data={"q": clean, "from": "en", "to": "zh-CHS"},
            headers={"User-Agent": "YoudaoDict/7.2.0"},
            timeout=10,
        )
        data = resp.json()
        speak_url = data.get("speakUrl", "")
        if not speak_url:
            return ""

        # 下载音频
        audio_resp = requests.get(speak_url, timeout=15)
        audio_resp.raise_for_status()
        if len(audio_resp.content) < 100:
            return ""

        audio_b64 = base64.b64encode(audio_resp.content).decode("utf-8")
        _invoke("storeMediaFile", filename=filename, data=audio_b64)
        return f"[sound:{filename}]"
    except Exception:
        return ""


def add_sentence(chinese, english, grammar="", note="", deck_name=None):
    deck = deck_name or SENTENCE_DECK_NAME
    ensure_deck(deck)
    ensure_sentence_model()

    # 清理输入
    english = english.strip().replace("\n", " ").replace("\r", "")

    # 检查重复
    result = _invoke("findNotes", query=f'"deck:{deck}" "English:{english}"')
    if result and len(result) > 0:
        return False, "该句型已存在于牌组中"

    audio = download_sentence_audio(english)

    note_id = _invoke(
        "addNote",
        note={
            "deckName": deck,
            "modelName": SENTENCE_MODEL_NAME,
            "fields": {
                "Chinese": chinese,
                "English": english,
                "Grammar": grammar,
                "Note": note,
                "Audio": audio,
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": deck,
                    "checkChildren": False,
                },
            },
        },
    )
    return True, note_id
