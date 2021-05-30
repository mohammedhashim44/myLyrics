from typing import Optional


def isEmptyOrNone(text: Optional[str]) -> bool:
    if text == "": return True
    if text is None: return True
    return False


def isBlankOrNone(text: Optional[str]) -> bool:
    if text is None: return True
    return isEmptyOrNone(text.strip())
