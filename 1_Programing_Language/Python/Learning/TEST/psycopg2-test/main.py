import psycopg2

db_config = {
    "host": "localhost",
    "port": "5432",
    "database": "postgres",
    "user": "postgres"
}

connection = psycopg2.connect(**db_config)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, name VARCHAR(50))")

cursor.execute("INSERT INTO test (name) VALUES (%s)", ("John Doe",))
connection.commit()
cursor.execute("SELECT * FROM test")
result = cursor.fetchall()
print(result)

cursor.execute("DELETE FROM test WHERE id = %s", (1,))
connection.commit()
cursor.execute("SELECT * FROM test")
result = cursor.fetchall()
print(result)

cursor.execute("DROP TABLE test")
connection.commit()

cursor.close()
connection.close()