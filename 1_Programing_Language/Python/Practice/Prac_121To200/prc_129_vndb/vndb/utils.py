import re
from typing import List


def judge_sexual(sexual: float) -> bool:
    if (sexual > 1):
        return True
    return False

def judge_violence(violence: float) -> bool:
    if (violence > 1):
        return True
    return False

def check_date(date_str: str) -> bool:
    # date should match format YYYY-MM-DD or YYYY-MM or YYYY
    match = re.match(r"^(\d{4})(-\d{2})?(-\d{2})?$", date_str)
    if not match:
        return False
    year, month, day = match.groups()
    if year:
        year = int(year)
        if year < 1980 or year > 2100:
            return False
    if month:
        month = int(month[1:])
        if month < 1 or month > 12:
            return False
    if day:
        month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if year % 4 == 0 and (year % 100!= 0 or year % 400 == 0):
            month_days[1] = 29
        day = int(day[1:])
        if day < 1 or day > month_days[month - 1]:
            return False
    return True

def format_description(description: str) -> str:
    if description is None:
        return ""
    description = re.sub(r"\[url=.*?\](.*?)\[/url\]", r"\1", description)
    description = re.sub(r"\[([bis])\](.*?)\[/\1\]", r"\2", description)
    description = re.sub(r"\[.*?\]", "", description)
    return description
