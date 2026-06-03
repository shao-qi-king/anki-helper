import argparse
import sys
import io

if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from youdao import lookup
from anki_connect import add_note

try:
    from colorama import init, Fore, Style
    init()
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    DIM = Style.DIM
    RESET = Style.RESET_ALL
except ImportError:
    GREEN = RED = YELLOW = CYAN = DIM = RESET = ""


def print_word_info(info):
    print(f"\n  {CYAN}{info['word']}{RESET}")
    if info["phonetic"]:
        print(f"  {DIM}{info['phonetic']}{RESET}")
    if info["definition"]:
        print(f"  {info['definition']}")
    if info["example"]:
        print(f"  {DIM}{info['example']}{RESET}")
    print()


def manual_input(word):
    """当 API 查不到时，手动输入释义"""
    print(f"  {YELLOW}未找到 '{word}' 的释义，请手动输入：{RESET}")
    phonetic = input("  音标（可跳过）: ").strip()
    definition = input("  释义: ").strip()
    example = input("  例句（可跳过）: ").strip()
    if not definition:
        print(f"  {RED}释义不能为空，取消添加{RESET}")
        return None
    return {
        "word": word,
        "phonetic": f"/{phonetic}/" if phonetic else "",
        "definition": definition,
        "example": example,
        "found": True,
    }


def cmd_add(args):
    word = args.word.strip().lower()
    info = lookup(word)

    if not info["found"]:
        info = manual_input(word)
        if not info:
            return

    print_word_info(info)

    try:
        success, result = add_note(
            word=info["word"],
            phonetic=info["phonetic"],
            definition=info["definition"],
            example=info["example"],
            note=args.note or "",
        )
        if success:
            print(f"  {GREEN}+ 已添加到牌组{RESET}")
        else:
            print(f"  {YELLOW}! {result}{RESET}")
    except (ConnectionError, RuntimeError) as e:
        print(f"  {RED}x {e}{RESET}")
        sys.exit(1)


def cmd_search(args):
    word = args.word.strip().lower()
    info = lookup(word)

    if not info["found"]:
        print(f"  {YELLOW}未找到 '{word}'{RESET}")
        return

    print_word_info(info)


def cmd_batch(args):
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"  {RED}文件不存在: {args.file}{RESET}")
        sys.exit(1)

    print(f"  共 {len(words)} 个单词\n")
    added = 0
    skipped = 0
    failed = 0

    for word in words:
        word = word.lower()
        info = lookup(word)
        if not info["found"]:
            print(f"  {YELLOW}- {word} (未找到释义，跳过){RESET}")
            failed += 1
            continue

        try:
            success, result = add_note(
                word=info["word"],
                phonetic=info["phonetic"],
                definition=info["definition"],
                example=info["example"],
            )
            if success:
                print(f"  {GREEN}+ {word}{RESET}")
                added += 1
            else:
                print(f"  {DIM}= {word} (已存在){RESET}")
                skipped += 1
        except (ConnectionError, RuntimeError) as e:
            print(f"  {RED}x {word} ({e}){RESET}")
            failed += 1

    print(f"\n  完成: 添加 {added}, 跳过 {skipped}, 失败 {failed}")


def main():
    parser = argparse.ArgumentParser(
        description="Anki 单词助手 - 快速添加英语单词到 Anki"
    )
    subparsers = parser.add_subparsers(dest="command")

    # add 命令
    add_parser = subparsers.add_parser("add", help="查词并添加到 Anki")
    add_parser.add_argument("word", help="要添加的单词")
    add_parser.add_argument("-n", "--note", help="附加备注", default="")

    # search 命令
    search_parser = subparsers.add_parser("search", help="只查词，不添加")
    search_parser.add_argument("word", help="要查询的单词")

    # batch 命令
    batch_parser = subparsers.add_parser("batch", help="从文件批量导入")
    batch_parser.add_argument("file", help="单词文件路径（一行一个）")

    args = parser.parse_args()

    if args.command == "add":
        cmd_add(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "batch":
        cmd_batch(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
