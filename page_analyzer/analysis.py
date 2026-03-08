import requests
from bs4 import BeautifulSoup


def analyze_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = BeautifulSoup(response.text, 'html.parser')
        status_code = response.status_code
        h1 = extract_h1(data)
        title = extract_title(data)
        description = extract_description(data)
        return status_code, h1, title, description
    except requests.exceptions.Timeout:
        print("Ошибка: время ожидания ответа истекло")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка HTTP: {e}")
        return None
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return None


def extract_h1(data):
    h1 = data.find('h1')
    if h1:
        result = h1.get_text(strip=True)
        return result
    return None


def extract_title(data):
    title = data.find('title')
    if title:
        result = title.get_text(strip=True)
        return result
    return None


def extract_description(data):
    description = data.find('meta', attrs={'name': 'description'})
    if description:
        if description.get('content'):
            result = description['content'].strip()
            if result:
                return result
    return None