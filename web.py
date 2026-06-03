import json
from flask import Flask, request, jsonify, send_from_directory
from youdao import lookup
from anki_connect import add_note, add_sentence, _invoke, check_duplicate, get_deck_names
from config import DECK_NAME, SENTENCE_DECK_NAME

app = Flask(__name__, static_folder="static")
app.config["JSON_AS_ASCII"] = False


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/search", methods=["POST"])
def api_search():
    word = request.json.get("word", "").strip()
    if not word:
        return jsonify({"error": "请输入单词"}), 400

    info = lookup(word)
    return jsonify(info)


@app.route("/api/decks", methods=["GET"])
def api_decks():
    try:
        decks = get_deck_names()
        decks = [d for d in decks if d != "Default"]
        decks.sort()
        return jsonify({"decks": decks, "default": DECK_NAME})
    except (ConnectionError, RuntimeError) as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/add", methods=["POST"])
def api_add():
    data = request.json
    word = data.get("word", "").strip()
    phonetic = data.get("phonetic", "")
    definition = data.get("definition", "")
    example = data.get("example", "")
    note = data.get("note", "")
    deck = data.get("deck", "")

    if not word or not definition:
        return jsonify({"error": "单词和释义不能为空"}), 400

    try:
        success, result = add_note(word, phonetic, definition, example, note, deck_name=deck or None)
        if success:
            return jsonify({"success": True, "message": "添加成功"})
        else:
            return jsonify({"success": False, "message": result})
    except (ConnectionError, RuntimeError) as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/words", methods=["GET"])
def api_words():
    deck = request.args.get("deck", DECK_NAME)
    try:
        note_ids = _invoke("findNotes", query=f'"deck:{deck}"')
        if not note_ids:
            return jsonify([])

        notes_info = _invoke("notesInfo", notes=note_ids)
        words = []
        for note in notes_info:
            fields = note.get("fields", {})
            words.append({
                "id": note["noteId"],
                "word": fields.get("Word", {}).get("value", ""),
                "phonetic": fields.get("Phonetic", {}).get("value", ""),
                "definition": fields.get("Definition", {}).get("value", ""),
                "example": fields.get("Example", {}).get("value", ""),
                "note": fields.get("Note", {}).get("value", ""),
            })
        words.sort(key=lambda x: x["word"])
        return jsonify(words)
    except (ConnectionError, RuntimeError) as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/delete", methods=["POST"])
def api_delete():
    note_id = request.json.get("id")
    if not note_id:
        return jsonify({"error": "缺少 id"}), 400

    try:
        _invoke("deleteNotes", notes=[note_id])
        return jsonify({"success": True})
    except (ConnectionError, RuntimeError) as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/sentence/add", methods=["POST"])
def api_sentence_add():
    data = request.json
    chinese = data.get("chinese", "").strip()
    english = data.get("english", "").strip()
    grammar = data.get("grammar", "").strip()
    note = data.get("note", "")
    deck = data.get("deck", "")

    if not chinese or not english:
        return jsonify({"error": "中文和英文都不能为空"}), 400

    try:
        success, result = add_sentence(chinese, english, grammar, note, deck_name=deck or None)
        if success:
            return jsonify({"success": True, "message": "添加成功"})
        else:
            return jsonify({"success": False, "message": result})
    except (ConnectionError, RuntimeError) as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/sentence/translate", methods=["POST"])
def api_sentence_translate():
    """翻译中文句子为英文"""
    chinese = request.json.get("chinese", "").strip()
    if not chinese:
        return jsonify({"error": "请输入中文"}), 400

    import requests as req
    result = {"chinese": chinese, "english": "", "found": False}

    try:
        resp = req.post(
            "https://aidemo.youdao.com/trans",
            data={"q": chinese, "from": "zh-CHS", "to": "en"},
            headers={"User-Agent": "YoudaoDict/7.2.0"},
            timeout=10,
        )
        data = resp.json()
        translations = data.get("translation", [])
        if translations:
            result["english"] = translations[0]
            result["found"] = True
    except Exception:
        pass

    return jsonify(result)


if __name__ == "__main__":
    print("Anki 单词助手已启动: http://localhost:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
