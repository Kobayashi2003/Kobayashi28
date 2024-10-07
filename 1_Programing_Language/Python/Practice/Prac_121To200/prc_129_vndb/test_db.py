def test_db_insert():
    import psycopg2
    import json
    from vndb.utils import generate_filters, generate_fields, search_vndb

    filters = generate_filters(developer='あざらしそふと')

    fields = generate_fields()
    results = search_vndb(filters=filters, fields=fields)['results']

    conn = psycopg2.connect(
        user     = 'postgres',
        password = 'root',
        database = 'flask_db',
        host     = 'localhost',
        port     = '5432'
    )
    with conn.cursor() as curs:
        for result in results:
            curs.execute("DELETE FROM vn WHERE id = %s", (result['id'],))
            curs.execute("INSERT INTO vn (id) VALUES (%s)", (result['id'],))
            curs.execute("UPDATE vn SET released = %s WHERE id = %s", (result['released'], result['id']))
            curs.execute("UPDATE vn SET length = %s WHERE id = %s", (result['length'], result['id']))
            curs.execute("UPDATE vn SET length_minutes = %s WHERE id = %s", (result['length_minutes'], result['id']))
            curs.execute("UPDATE vn SET title = %s WHERE id = %s", (result['title'], result['id']))
            curs.execute("UPDATE vn SET titles = %s WHERE id = %s", (json.dumps(result['titles']), result['id']))
            curs.execute("UPDATE vn SET developers = %s WHERE id = %s", (json.dumps(result['developers']), result['id']))
            curs.execute("UPDATE vn SET platforms = %s WHERE id = %s", (json.dumps(result['platforms']), result['id']))
            curs.execute("UPDATE vn SET image = %s WHERE id = %s", (json.dumps(result['image']), result['id']))
            curs.execute("UPDATE vn SET screenshots = %s WHERE id = %s", (json.dumps(result['screenshots']), result['id']))
            curs.execute("UPDATE vn SET data = %s WHERE id = %s", (json.dumps(result), result['id']))
    conn.commit()
    print('Done')

def test_db_select():
    import psycopg2
    import json

    conn = psycopg2.connect(
        user     = 'postgres',
        password = 'root',
        database = 'flask_db',
        host     = 'localhost',
        port     = '5432'
    )
    with conn.cursor() as curs:
        curs.execute("SELECT data FROM vn WHERE id = 'v19073'") # 千恋万花
        result = curs.fetchone()
        if result is None:
            print('VN not found')
            return
        print(result[0])


if __name__ == '__main__':
    test_db_insert()
    # test_db_select()
