import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from page_analyzer.controllers import normalize_url, validate_url
from page_analyzer.models import URL, URLCheck

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def add_url():
    url = request.form.get('url', '').strip()
    is_valid, error = validate_url(url)
    if not is_valid:
        flash(error, 'danger')
        return render_template('index.html'), 422
    normalized_url = normalize_url(url)
    url_id, is_new = URL.save(normalized_url)
    if is_new:
        flash('Страница успешно добавлена', 'success')
    else:
        flash('Страница уже существует', 'info')
    return redirect(url_for('show_url', id=url_id))


@app.route('/urls/<int:id>')
def show_url(id):
    find_url = URL.find(id)
    if not find_url:
        flash('URL не указан', 'danger')
        return redirect(url_for('index'))
    find_checks = URLCheck.find_checks(id)
    return render_template('url.html', url=find_url, checks=find_checks)


@app.route('/urls')
def get_urls():
    all_urls = URL.all()
    return render_template('urls.html', urls=all_urls)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def add_check_url(id):
    url = URL.find(id)
    if not url:
        flash('URL не найден', 'danger')
        return redirect(url_for('index'))
    URLCheck.save(id)
    flash('Проверка URL успешно добавлена', 'success')
    return redirect(url_for('show_url', id=id))


@app.template_filter('datetime')
def format_datetime(datetime, format='%Y-%m-%d %H:%M:%S'):
    if datetime:
        return datetime.strftime(format)
    return ''