import hashlib
import time
import uuid
import requests

YOUDAO_API_URL = "https://dict.youdao.com/jsonapi_s?doctype=json&jsonversion=4"


def _query_youdao_free(word):
    """使用有道词典免费接口查询单词"""
    url = f"https://dict.youdao.com/suggest?num=1&ver=3.0&doctype=json&cache=false&le=en&q={word}"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException:
        return None


def _query_youdao_dict(word):
    """使用有道词典网页接口获取详细信息"""
    url = f"https://dict.youdao.com/jsonapi?jsonversion=2&client=mobile&q={word}&dicts=%7B%22count%22%3A99%7D&keyfrom=mdict.7.2&model=honor&mid=5.6.1&imei=659135764921685&vendor=wandoujia&screen=1080x1920&ssid=superman&abtest=3"
    headers = {
        "User-Agent": "YoudaoDict/7.2.0 (Android; 5.0)"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException:
        return None


def lookup(word):
    """
    查询单词（支持英文查中文、中文查英文），返回字典：
    {
        "word": str,
        "phonetic": str,
        "definition": str,
        "example": str,
        "found": bool
    }
    """
    result = {
        "word": word,
        "phonetic": "",
        "definition": "",
        "example": "",
        "found": False,
    }

    data = _query_youdao_dict(word)
    if not data:
        return result

    is_chinese = any('一' <= c <= '鿿' for c in word)

    if is_chinese:
        # 中文查英文：解析 ce 部分
        ce = data.get("ce", {})
        first_en_word = ""
        if ce:
            word_info = ce.get("word", {})
            if isinstance(word_info, list) and word_info:
                word_info = word_info[0]

            trs = word_info.get("trs", [])
            definitions = []
            for tr in trs:
                if "tr" in tr:
                    for item in tr["tr"]:
                        l_data = item.get("l", {})
                        # 提取英文词：从 i 列表中拼接
                        i_list = l_data.get("i", [])
                        en_word = ""
                        for part in i_list:
                            if isinstance(part, str):
                                en_word += part
                            elif isinstance(part, dict) and "#text" in part:
                                en_word += part["#text"]
                        en_word = en_word.strip()
                        # 提取中文翻译
                        tran = l_data.get("#tran", "")
                        pos = l_data.get("pos", "")
                        if en_word:
                            if not first_en_word:
                                first_en_word = en_word
                            line = f"{pos} {en_word}".strip()
                            if tran:
                                line += f"  ({tran.split('；')[0]})"
                            definitions.append(line)
            if definitions:
                result["definition"] = "\n".join(definitions)
                result["found"] = True

        # 用第一个英文单词二次查询获取音标
        if first_en_word:
            en_data = _query_youdao_dict(first_en_word)
            if en_data:
                ec = en_data.get("ec", {})
                if ec:
                    en_word_info = ec.get("word", {})
                    if isinstance(en_word_info, list) and en_word_info:
                        en_word_info = en_word_info[0]
                    usphone = en_word_info.get("usphone", "")
                    ukphone = en_word_info.get("ukphone", "")
                    if usphone:
                        result["phonetic"] = f"/{usphone}/"
                    elif ukphone:
                        result["phonetic"] = f"/{ukphone}/"

        # ce 没结果，用 fanyi
        if not result["found"]:
            fanyi = data.get("fanyi", {})
            if fanyi:
                tran = fanyi.get("tran", "")
                if tran:
                    result["definition"] = tran
                    result["found"] = True
    else:
        # 英文查中文：解析 ec 部分
        ec = data.get("ec", {})
        if ec:
            word_info = ec.get("word", {})
            if isinstance(word_info, list) and word_info:
                word_info = word_info[0]

            usphone = word_info.get("usphone", "")
            ukphone = word_info.get("ukphone", "")
            if usphone:
                result["phonetic"] = f"/{usphone}/"
            elif ukphone:
                result["phonetic"] = f"/{ukphone}/"

            trs = word_info.get("trs", [])
            definitions = []
            for tr in trs:
                if "tr" in tr:
                    for item in tr["tr"]:
                        if "l" in item and "i" in item["l"]:
                            definitions.append(item["l"]["i"][0])
            if definitions:
                result["definition"] = "\n".join(definitions)
                result["found"] = True

        if not result["found"]:
            fanyi = data.get("fanyi", {})
            if fanyi:
                tran = fanyi.get("tran", "")
                if tran:
                    result["definition"] = tran
                    result["found"] = True

    # 提取例句
    blng_sents = data.get("blng_sents_part", {})
    if blng_sents:
        pairs = blng_sents.get("sentence-pair", [])
        if pairs:
            first = pairs[0]
            en_sent = first.get("sentence", "").strip()
            cn_sent = first.get("sentence-translation", "").strip()
            if en_sent:
                result["example"] = f"{en_sent}\n{cn_sent}"

    return result
