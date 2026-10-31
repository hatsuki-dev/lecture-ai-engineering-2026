"""第1回: 素のLLMに質問し、会話履歴を保ちながら続けて対話するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると対話モードになる
    uv run python -m app.ask --continue  # 会話履歴を保ったまま入力を続ける

素のLLM でも、同じ chat セッションを使えば前の質問を記憶したまま回答し続けられる。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
import time

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def print_usage(response, elapsed_seconds: float | None = None) -> None:
    """応答時間とトークン数を表示する。"""

    if elapsed_seconds is not None:
        print(f"[time] {elapsed_seconds:.3f} s")

    usage = getattr(response, "usage_metadata", None)
    if usage is None:
        return

    prompt_tokens = getattr(usage, "prompt_token_count", None)
    output_tokens = getattr(usage, "candidates_token_count", None)
    total_tokens = getattr(usage, "total_token_count", None)
    if any(value is not None for value in (prompt_tokens, output_tokens, total_tokens)):
        summary = (
            f"入力={prompt_tokens if prompt_tokens is not None else 0} "
            f"/ 出力={output_tokens if output_tokens is not None else 0}"
        )
        if total_tokens is not None:
            summary += f" / 合計={total_tokens}"
        print(f"[tokens] {summary}")


def create_chat(model_name: str | None = None):
    """会話履歴を持てる Chat セッションを新規作成する。"""
    client = genai.Client(api_key=get_api_key())
    return client.chats.create(model=model_name or MODEL)


def ask(question: str, chat=None, model_name: str | None = None) -> str:
    """既存の chat セッションがあればそれを使い、なければ新しいセッションを作る。"""
    if chat is None:
        chat = create_chat(model_name=model_name)

    start = time.perf_counter()
    response = chat.send_message(question)
    elapsed = time.perf_counter() - start
    print_usage(response, elapsed)
    return response.text


def run_interactive_chat(model_name: str | None = None) -> None:
    """会話履歴を維持したまま、複数の質問を続けて入力できる。"""
    active_model = model_name or MODEL

    with genai.Client(api_key=get_api_key()) as client:
        chat = client.chats.create(model=active_model)

        print(f"[model] {active_model}")
        print("会話を開始します。終了するには 'exit'、'quit'、または 'q' を入力してください。\n")

        while True:
            try:
                question = input("質問> ").strip()
            except EOFError:
                print()
                break

            if not question:
                continue

            if question.lower() in {"exit", "quit", "q"}:
                break

            try:
                print(ask(question, chat=chat, model_name=active_model))
            except errors.APIError as e:
                print(api_error_message(e.code, e.message))
                break


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=None)
    parser.add_argument("--continue", dest="continue_chat", action="store_true", help="会話履歴を保ったまま、継続的に質問する")
    args = parser.parse_args()

    if args.continue_chat or args.question is None:
        run_interactive_chat()
        return
    
    with genai.Client(api_key=get_api_key()) as client:
        chat = client.chats.create(model=MODEL)
        print(f"[model] {MODEL}")
        print(f"[質問] {args.question}\n")

        try:
            print(ask(args.question, chat=chat))
        except errors.APIError as e:
            print(api_error_message(e.code, e.message))
            raise SystemExit(1)


if __name__ == "__main__":
    main()
