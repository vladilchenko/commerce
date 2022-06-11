from typing import Union


def get_category(category: str) -> Union[str, None]:
    """
    Search category in CATEGORIES list and returns human-readable name
    """
    CATEGORIES = [
        ("book", "Books"),
        ("video", "Videos"),
        ("audio", "Audios"),
        ("img", "Images"),
        ("other", "Other")
    ]

    for item in CATEGORIES:
        if category == item[0]:
            return item[1]
