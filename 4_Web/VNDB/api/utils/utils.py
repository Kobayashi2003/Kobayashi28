import re
import datetime


def judge_sexual(sexual: float) -> bool:
    return sexual > 1

def judge_violence(violence: float) -> bool:
    return violence > 1

def check_date(date_str: str) -> bool:
    patterns = [
        (r"^\d{4}$", "%Y"),
        (r"^\d{4}-\d{2}$", "%Y-%m"),
        (r"^\d{4}-\d{2}-\d{2}$", "%Y-%m-%d")
    ]

    for pattern, fmt in patterns:
        if re.match(pattern=pattern, string=date_str):
            try:
                date = datetime.strptime(date_str, fmt)
                return 1980 <= date.year <= 2100
            except ValueError:
                return False
    
    return False

def format_description(description: str) -> str:
    if not description: return False

    replacements = {
        r"\[url=.*?\](.*?)\[/url\]": r"\1",
        r"\[([bis])\](.*?)\[/\1\]": r"\2",
        r"\[.*?\]": ""
    }
    
    for pattern, repl in replacements.items():
        description = re.sub(pattern, repl, description)
    
    return description