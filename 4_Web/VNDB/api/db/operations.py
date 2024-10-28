import json
import psycopg2
from typing import Dict, Any, List, Optional, Tuple
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

def create(vn_data: Dict[str, Any]) -> bool:
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            vn_id = vn_data['id']
            query = "INSERT INTO vn (id, data) VALUES (%s, %s)"
            cur.execute(query, (vn_id, json.dumps(vn_data)))
            conn.commit()
        db_logger.info(f"Created new VN with ID: {vn_id}")
        return True
    except (Exception, psycopg2.Error) as error:
        conn.rollback()
        db_logger.error(f"Error creating new VN: {error}")
        return False
    finally:
        release_db_connection(conn)

def delete(vn_id: str) -> bool:
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "DELETE FROM vn WHERE id = %s"
            cur.execute(query, (vn_id,))
            rows_affected = cur.rowcount
            conn.commit()
        db_logger.info(f"Deleted VN with ID: {vn_id}. Rows affected: {rows_affected}")
        return rows_affected > 0
    except (Exception, psycopg2.Error) as error:
        conn.rollback()
        db_logger.error(f"Error deleting VN with ID {vn_id}: {error}")
        return False
    finally:
        release_db_connection(conn)

def update(vn_id: str, vn_data: Optional[Dict[str, Any]] = None, downloaded: Optional[bool] = None) -> bool:
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if vn_data is not None:
                query = "UPDATE vn SET data = data || %s::jsonb WHERE id = %s"
                cur.execute(query, (json.dumps(vn_data), vn_id))
            if downloaded is not None:
                query = "UPDATE vn SET downloaded = %s WHERE id = %s"
                cur.execute(query, (downloaded, vn_id))
            
            rows_affected = cur.rowcount
            conn.commit()
        
        if vn_data is not None and downloaded is not None:
            db_logger.info(f"Updated VN with ID: {vn_id}. Full data update and downloaded status: {downloaded}. Rows affected: {rows_affected}")
        elif vn_data is not None:
            db_logger.info(f"Updated VN with ID: {vn_id}. Full data update. Rows affected: {rows_affected}")
        elif downloaded is not None:
            db_logger.info(f"Updated VN with ID: {vn_id}. Downloaded status: {downloaded}. Rows affected: {rows_affected}")
        
        return rows_affected > 0
    except (Exception, psycopg2.Error) as error:
        conn.rollback()
        db_logger.error(f"Error updating VN with ID {vn_id}: {error}")
        return False
    finally:
        release_db_connection(conn)

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
 