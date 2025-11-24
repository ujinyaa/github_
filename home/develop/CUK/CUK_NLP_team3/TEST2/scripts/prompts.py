
EXPLICIT_RULE_CARD_A = """[RULES]
1) SOV word order (Subject–Object–Verb).
2) The suffix -ka attaches only to A-class nouns.
"""

EXPLICIT_RULE_CARD_B = """[RULES]
In this language, sentences follow SOV word order.
That means the subject comes first, then the object, and the verb comes at the end.
The suffix -ka attaches only to a specific class of nouns (A-class nouns).
"""

EXPLICIT_RULE_CARD_C = """[RULES]
Remember: the pattern is always Subject → Object → Verb (SOV).
Think of it as 'who does what to whom', with the action (verb) coming last.
Also remember: the suffix -ka only appears on A-class nouns, not on every noun.
"""

EXAMPLES = """[EXAMPLE]
mika-ka ... ✓
miti-ka ... ✗
"""



def build_prompt(
    ex: dict,
    condition: str = "implicit",
    for_eval: bool = False,
    task_type: str = "generation",
    rule_variant: str = "a",   # "a" / "b" / "c" (기본값: a)
) -> str:

    if for_eval:
        return ex.get("text", "") or ex.get("sentence", "")

    sent = (
        ex.get("text")
        or ex.get("text_pos")
        or ex.get("sentence")
        or ex.get("text_neg", "")
    )

    meta = ex.get("meta", {}) or {}

    rule_variant = meta.get("rule_variant", rule_variant)

    condition = (condition or "").lower()

    if condition == "explicit":
        if rule_variant == "a":
            rule_card = EXPLICIT_RULE_CARD_A
        elif rule_variant == "b":
            rule_card = EXPLICIT_RULE_CARD_B
        elif rule_variant == "c":
            rule_card = EXPLICIT_RULE_CARD_C
        else:
            rule_card = EXPLICIT_RULE_CARD_A

        rule_section = f"{rule_card}\n{EXAMPLES}"

    else:
        rule_card = ""
        rule_section = f"{EXAMPLES}"

    # use_rules: False 이면 규칙 카드 제거
    use_rules = meta.get("use_rules", True if condition == "explicit" else False)
    use_examples = meta.get("use_examples", True)

    if not use_rules:
        rule_section = rule_section.replace(EXPLICIT_RULE_CARD_A, "")
        rule_section = rule_section.replace(EXPLICIT_RULE_CARD_B, "")
        rule_section = rule_section.replace(EXPLICIT_RULE_CARD_C, "")

    if not use_examples:
        rule_section = rule_section.replace(EXAMPLES, "")

    rule_section = rule_section.strip()
    if rule_section:
        rule_section = rule_section + "\n"

    if task_type == "generation":
        prompt = f"{rule_section}[INPUT]\n{sent}"

    elif task_type == "grammaticality":
        prompt = (
            f"{rule_section}"
            f"[TASK]\n"
            f"Judge whether the following sentence is grammatically correct "
            f"according to the given rules (if any).\n"
            f"[SENTENCE]\n{sent}\n"
            f"Answer with 'Yes' if it is grammatical, or 'No' if it violates the rule."
        )

    elif task_type == "comparison":
        s1, s2 = ex.get("sentence_1"), ex.get("sentence_2")
        prompt = (
            f"{rule_section}"
            f"[TASK]\n"
            f"Which of the following sentences is grammatically correct?\n"
            f"1. {s1}\n2. {s2}\n"
            f"Answer with '1' or '2'."
        )

    elif task_type == "mcq":
        options = ex.get("options", [])
        question = ex.get("question", "Choose the grammatically correct sentence:")
        opts = "\n".join(f"{i+1}. {o}" for i, o in enumerate(options))
        prompt = (
            f"{rule_section}"
            f"[TASK]\n{question}\n"
            f"{opts}\n"
            f"Answer with '1', '2', '3', '4', or '5'."
        )

    else:
        raise ValueError(f"Unknown task_type: {task_type}")

    return prompt
