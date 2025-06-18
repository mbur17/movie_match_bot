import re
from datetime import datetime, timedelta


def is_valid_release_date(release_date_str: str) -> bool:
    try:
        release_date = datetime.fromisoformat(release_date_str)
        return release_date <= datetime.now() - timedelta(days=1)
    except (ValueError, TypeError):
        return False


def is_russian_text(text: str, min_letters: int = 3) -> bool:
    if not text:
        return False
    russian_letters = re.findall(r'[а-яА-ЯёЁ]', text)
    return len(russian_letters) >= min_letters
