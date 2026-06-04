ANKI_CONNECT_URL = "http://localhost:8765"
DECK_NAME = "English Vocabulary"
MODEL_NAME = "English Vocabulary"
SENTENCE_MODEL_NAME = "English Sentences"
SENTENCE_DECK_NAME = "English Sentences"

LISTENING_MODEL_NAME = "English Listening"
LISTENING_DECK_NAME = "English Listening"

CARD_FRONT_TEMPLATE = """<div class="word">{{Word}}</div>
<div class="phonetic">{{Phonetic}}</div>
{{Audio}}"""

CARD_BACK_TEMPLATE = """<div class="word">{{Word}}</div>
<div class="phonetic">{{Phonetic}}</div>
{{Audio}}
<hr>
<div class="definition">{{Definition}}</div>
<div class="example">{{Example}}</div>
{{#Note}}<div class="note">{{Note}}</div>{{/Note}}"""

SENTENCE_FRONT_TEMPLATE = """<div class="chinese">{{Chinese}}</div>
{{#Grammar}}<div class="grammar-hint">语法: {{Grammar}}</div>{{/Grammar}}
<div class="hint">试着说出英文，然后翻面对答案</div>"""

SENTENCE_BACK_TEMPLATE = """<div class="chinese">{{Chinese}}</div>
<hr>
<div class="english">{{English}}</div>
{{Audio}}
{{#Grammar}}<div class="grammar">{{Grammar}}</div>{{/Grammar}}
{{#Note}}<div class="note">{{Note}}</div>{{/Note}}"""

CARD_CSS = """
.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 18px;
    text-align: center;
    color: #333;
    background: #fafafa;
    padding: 20px;
}
.word {
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 10px;
}
.phonetic {
    color: #666;
    font-size: 16px;
    margin-bottom: 12px;
}
.definition {
    font-size: 20px;
    margin-bottom: 12px;
    text-align: left;
    padding: 0 20px;
}
.example {
    color: #555;
    font-style: italic;
    font-size: 16px;
    margin-top: 10px;
    text-align: left;
    padding: 0 20px;
}
.note {
    color: #888;
    font-size: 14px;
    margin-top: 12px;
    border-top: 1px dashed #ddd;
    padding-top: 8px;
}
"""

SENTENCE_CSS = """
.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 18px;
    text-align: center;
    color: #333;
    background: #fafafa;
    padding: 30px 20px;
}
.chinese {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 16px;
    line-height: 1.5;
}
.english {
    font-size: 22px;
    color: #1a73e8;
    font-weight: 500;
    margin-bottom: 14px;
    line-height: 1.5;
}
.grammar {
    font-size: 14px;
    color: #666;
    margin-top: 12px;
    padding: 10px 16px;
    background: #f0f4ff;
    border-radius: 8px;
    text-align: left;
}
.grammar-hint {
    font-size: 13px;
    color: #999;
    margin-top: 8px;
}
.hint {
    font-size: 13px;
    color: #bbb;
    margin-top: 20px;
}
.note {
    color: #888;
    font-size: 14px;
    margin-top: 12px;
    border-top: 1px dashed #ddd;
    padding-top: 8px;
}
.replay-button svg { width: 32px; height: 32px; }
.replay-button { margin-top: 10px; }
"""

LISTENING_FRONT_TEMPLATE = """{{Audio}}
<div class="listen-hint">听音辨词</div>"""

LISTENING_BACK_TEMPLATE = """<div class="word">{{Word}}</div>
<div class="phonetic">{{Phonetic}}</div>
{{Audio}}
<hr>
<div class="definition">{{Definition}}</div>
<div class="example">{{Example}}</div>
{{#Note}}<div class="note">{{Note}}</div>{{/Note}}"""

LISTENING_CSS = """
.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 18px;
    text-align: center;
    color: #333;
    background: #fafafa;
    padding: 40px 20px;
}
.listen-hint {
    font-size: 14px;
    color: #bbb;
    margin-top: 24px;
}
.word {
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 10px;
}
.phonetic {
    color: #666;
    font-size: 16px;
    margin-bottom: 12px;
}
.definition {
    font-size: 20px;
    margin-bottom: 12px;
    text-align: left;
    padding: 0 20px;
}
.example {
    color: #555;
    font-style: italic;
    font-size: 16px;
    margin-top: 10px;
    text-align: left;
    padding: 0 20px;
}
.note {
    color: #888;
    font-size: 14px;
    margin-top: 12px;
    border-top: 1px dashed #ddd;
    padding-top: 8px;
}
.replay-button svg { width: 48px; height: 48px; }
.replay-button { margin-top: 10px; }
"""
