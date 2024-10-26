import json
import psycopg2
from flask import g, current_app
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from api.utils.logger import db_logger 
from api.utils.logger import test_logger

class DatabasePool:
    _pool = None

    @classmethod
    def get_pool(cls):
        return cls._pool

    @classmethod
    def init_pool(cls, **kwargs):
        try:
            cls._pool = psycopg2.pool.SimpleConnectionPool(1, 20, **kwargs)
            db_logger.info("Database connection pool initialized successfully.")
        except (Exception, psycopg2.Error) as error:
            db_logger.error(f"Error initializing database connection pool: {error}", exc_info=True)
            raise
    
def init_app(app):
    db_config = {
        'dbname': app.config['DB_NAME'],
        'user': app.config['DB_USER'],
        'password': app.config['DB_PASSWORD'],
        'host': app.config['DB_HOST'],
        'port': app.config['DB_PORT']
    }
    DatabasePool.init_pool(**db_config)

def get_db_connection():
    return DatabasePool.get_pool().getconn()

def release_db_connection(conn):
    DatabasePool.get_pool().putconn(conn)

def search(filters, fields, sort_field=None, reverse=False, limit=1000, offset=0):
    where_clauses = []
    params = []

    query = "SELECT %s FROM vn"
    params.append(fields)

    for where_clause, filter_params in filters:
        where_clauses.append(where_clause)
        params.extend(filter_params)

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    if sort_field:
        query += f" ORDER BY vn.data->>'{sort_field}' {'DESC' if reverse else 'ASC'}"
    
    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    test_logger.info(f"Executing query: {query}, params: {params}")
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            results = cur.fetchall()
        return [dict(row) for row in results]
    except (Exception, psycopg2.Error) as error:
        db_logger.error(f"Error executing search query: {error}")
        raise
    finally:
        release_db_connection(conn)