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
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, name, created_at FROM urls WHERE name = %s",  # noqa: E501
                    (url,)
                )
                data = cur.fetchone()
                if data:
                    return data[0], False
                cur.execute(
                    "INSERT INTO urls (name) VALUES (%s) RETURNING id, created_at",  # noqa: E501
                    (url,)
                )
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
