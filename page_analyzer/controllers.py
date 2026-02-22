from urllib.parse import urlparse
import validators


def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_url = f'{parsed_url.scheme}://{parsed_url.netloc}'.lower()
    return normalized_url


def validate_url(url):
    if not url:
        return False, 'URL не может быть пустым'
    if len(url) > 255:
        return False, 'Длина URL не может превышать 255 символов'
    if not validators.url(url):
        return False, 'Некорректный URL'
    return True, None