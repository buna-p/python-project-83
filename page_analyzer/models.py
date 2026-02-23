import os
from datetime import datetime

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_conn():
    return psycopg2.connect(DATABASE_URL)


class URL:
    def __init__(self, id=None, name=None, created_at=None):
        self.id = id
        self.name = name
        self.created_at = created_at or datetime.now()

    @staticmethod
    def save(url):
        select_query = "SELECT id, name, created_at FROM urls WHERE name = %s"
        insert_query = """INSERT INTO urls (name) VALUES (%s) 
        RETURNING id, created_at"""
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(select_query, (url,))
                data = cur.fetchone()
                if data:
                    return data[0], False
                cur.execute(insert_query, (url,))
                data = cur.fetchone()
                return data[0], True

    @staticmethod
    def find(id):
        with get_conn() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
                    "SELECT id, name, created_at FROM urls WHERE id = %s",
                    (id,)
                )
                data = cur.fetchone()
                if data:
                    return URL(
                        id=data['id'],
                        name=data['name'],
                        created_at=data['created_at']
                        )
                return None

    @staticmethod
    def all(order_by='created_at DESC'):
        with get_conn() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
                    f"SELECT id, name, created_at FROM urls ORDER BY {order_by}"
                    )
                data = cur.fetchall()
                return [URL(
                    id=note['id'],
                    name=note['name'],
                    created_at=note['created_at']
                    ) for note in data]

    @property
    def last_check(self):
        return URLCheck.get_last_check(self.id)


class URLCheck:
    def __init__(
            self,
            url_id,
            id=None,
            status_code=None,
            h1=None,
            title=None,
            description=None,
            created_at=None
            ):
        self.url_id = url_id
        self.id = id
        self.status_code = status_code
        self.h1 = h1
        self.title = title
        self.description = description
        self.created_at = created_at

    @staticmethod
    def save_check(url_id):
        insert_query = """INSERT INTO url_checks (url_id) VALUES (%s) 
        RETURNING id"""
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(insert_query, (url_id,))
                check_id = cur.fetchone()[0]
                conn.commit()
                return check_id

    @staticmethod
    def find_checks(url_id, order_by='created_at DESC'):
        select_query = f"""SELECT id, url_id, status_code, h1, title, description, created_at 
        FROM url_checks WHERE url_id = %s ORDER BY {order_by}"""  # noqa: E501
        with get_conn() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(select_query, (url_id,)) 
                data = cur.fetchall()
                return [
                    URLCheck(
                    id=note['id'],
                    url_id=note['url_id'],
                    status_code=note['status_code'],
                    h1=note['h1'],
                    title=note['title'],
                    description=note['description'],
                    created_at=note['created_at']
                    ) for note in data
                ]

    @staticmethod
    def get_last_check(url_id):
        select_query = """SELECT id, url_id, status_code, h1, title, description, created_at 
        FROM url_checks WHERE url_id = %s ORDER BY created_at DESC LIMIT 1"""  # noqa: E501
        with get_conn() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(select_query, (url_id,))
                data = cur.fetchone()
                if data:
                    return URLCheck(
                        id=data['id'],
                        url_id=data['url_id'],
                        status_code=data['status_code'],
                        h1=data['h1'],
                        title=data['title'],
                        description=data['description'],
                        created_at=data['created_at']
                    )
                return None

    @staticmethod
    def upd_check(id, status_code, h1, title, description):
        upd_query = """UPDATE url_checks 
        SET status_code=%s, h1=%s, title=%s, description=%s WHERE id=%s"""
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    upd_query,
                    (status_code, h1, title, description, id)
                    )
                conn.commit()
                return cur.rowcount > 0

    @staticmethod
    def del_check(id):
        del_query = "DELETE FROM url_checks WHERE id = %s"
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(del_query, (id,))
                conn.commit()
                return cur.rowcount > 0