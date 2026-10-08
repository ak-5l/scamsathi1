"""Pure helpers for parsing and reporting Gemma's outputs."""

import json
import re

ALLOWED_RISKS = {"HIGH", "MEDIUM", "LOW", "UNCERTAIN"}


def parse_analysis(raw: str) -> dict:
    """Parse structured text, tolerating Markdown JSON fences from an LLM."""
    content = raw.strip()
    content = re.sub(r"^```(?:json)?\s*", "", content, flags=re.IGNORECASE)
    content = re.sub(r"\s*```$", "", content)
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Fallback if the model places explanation around the JSON object.
        left = content.find("{")
        right = content.rfind("}")
        if left < 0 or right < left:
            raise ValueError("The model did not return valid structured output. Try again.")
        try:
            data = json.loads(content[left : right + 1])
        except json.JSONDecodeError as exc:
            raise ValueError("The model returned invalid JSON. Try again.") from exc

    if not isinstance(data, dict):
        raise ValueError("The model returned the wrong format. Try again.")
    level = str(data.get("risk_level", "UNCERTAIN")).strip().upper()
    if level not in ALLOWED_RISKS:
        level = "UNCERTAIN"

    def as_list(value):
        if not isinstance(value, list):
            return []
        return [item.strip() for item in value if isinstance(item, str) and item.strip()][:4]

    def as_text(value, fallback):
        return value.strip() if isinstance(value, str) and value.strip() else fallback

    return {
        "risk_level": level,
        "explanation": as_text(data.get("explanation"), "No explanation supplied."),
        "red_flags": as_list(data.get("red_flags")),
        "safe_steps": as_list(data.get("safe_steps")) or [
            "Verify the claim through an official phone number or website."
        ],
        "language": as_text(data.get("language"), "Unknown"),
    }


def format_report(message: str, result: dict, model: str) -> str:
    flags = "\n".join("- " + x for x in result["red_flags"]) or "None clearly identified"
    actions = "\n".join("- " + x for x in result["safe_steps"])
    return (
        "ScamSathi - Message screening (not a verification)\n"
        "==================================================\n"
        f"Model: {model}\n"
        f"Risk category: {result['risk_level']}\n"
        f"Language: {result['language']}\n\n"
        f"Analyzed message:\n{message}\n\n"
        f"Explanation:\n{result['explanation']}\n\n"
        f"Possible warning signs:\n{flags}\n\n"
        f"Safer steps:\n{actions}\n\n"
        "Disclaimer: AI predictions can be wrong. Check with an official source.\n"
    )
