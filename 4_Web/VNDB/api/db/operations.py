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
        if cls._pool is None:
            cls.init_pool()
        return cls._pool

    @classmethod
    def init_pool(cls):
        try:
            db_config = {
                'dbname': current_app.config['DB_NAME'],
                'user': current_app.config['DB_USER'],
                'password': current_app.config['DB_PASSWORD'],
                'host': current_app.config['DB_HOST'],
                'port': current_app.config['DB_PORT']
            }
            cls._pool = psycopg2.pool.SimpleConnectionPool(1, 20, **db_config)
            db_logger.info("Database connection pool initialized successfully.")
        except (Exception, psycopg2.Error) as error:
            db_logger.error(f"Error initializing database connection pool: {error}", exc_info=True)
            raise

def get_db_connection():
    if 'db_conn' not in g:
        g.db_conn = DatabasePool.get_pool().getconn()
    return g.db_conn

def release_db_connection(conn):
    if 'db_conn' in g:
        DatabasePool.get_pool().putconn(g.db_conn)
        g.pop('db_conn', None)

def init_app(app):
    app.teardown_appcontext(close_db)

def close_db(e=None):
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        DatabasePool.get_pool().putconn(db_conn)

def search(filters, fields, sort_field=None, reverse=False, limit=1000, offset=0):
    where_clauses = []
    params = []

    query = f"SELECT {fields} FROM vn" 

    for where_clause, filter_params in filters:
        where_clauses.append(where_clause)
        params.extend(filter_params)

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    if sort_field:
        query += f" ORDER BY vn.data->>'{sort_field}' {'DESC' if reverse else 'ASC'}"
    
    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            results = cur.fetchall()
        results = [dict(row) for row in results]
        return {
            'count': len(results),
            'results': results
        }
    except (Exception, psycopg2.Error) as error:
        db_logger.error(f"Error executing search query: {error}")
        raise
    finally:
        release_db_connection(conn)