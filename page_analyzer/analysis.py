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
    except Exception:
        return None


def extract_h1(data):
    h1 = data.find('h1')
    result = h1.get_text(strip=True)
    if result:
        return result
    return None


def extract_title(data):
    title = data.find('title')
    result = title.get_text(strip=True)
    if result:
        return result
    return None


def extract_description(data):
    description = data.find('meta', attrs={'name': 'description'})
    if description and description.get('content'):
        result = description['content'].strip()
    if result:
        return result
    return None