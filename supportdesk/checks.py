"""Behavioral checks: what the reply must do, or must never do. No word-for-word matching."""


def parts(response):
    text = " ".join(b.text for b in response.content if b.type == "text")
    tools = [b.name for b in response.content if b.type == "tool_use"]
    return text, tools


def calls_tool(response, name):
    return name in parts(response)[1], f"calls {name}"


def never_calls(response, name):
    return name not in parts(response)[1], f"never calls {name}"


def mentions(response, word):
    return word.lower() in parts(response)[0].lower(), f"mentions {word}"


def never_contains(response, word):
    return word not in parts(response)[0], f"never contains {word}"


def max_words(response, n):
    return len(parts(response)[0].split()) <= n, f"under {n} words"


CHECKS = {"calls_tool": calls_tool, "never_calls": never_calls, "mentions": mentions,
          "never_contains": never_contains, "max_words": max_words}
