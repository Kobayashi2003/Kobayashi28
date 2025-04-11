# import pytest
import sqlite3

con = sqlite3.connect('school_map.db')

# TABLE
# campus(int:campus_id(PK), text:campus_name, text:campus_addr, text:campus_area, text:campus_info, int:postal_code)
# building_type(building_type_id(PK), building_type_name)
# building(building_id(PK), building_name, building_number, building_type_id(FK), building_info, campus_id(FK))
# building_position(building_id(PK), x, y, width, height, map_width, map_height)
# road(road_id(PK), road_name, road_number, road_info, campus_id(FK))
# road_position(point_id(PK), road_id, point_x, point_y, point_radius, nxt_point_id, lst_point_id, point_info)

def test_campus():
    print('Test campus')
    cur = con.cursor()
    cur.execute('SELECT * FROM campus')
    for line in cur.fetchall():
        print(line)
    print()

def test_building_type():
    print('Test building_type')
    cur = con.cursor()
    cur.execute('SELECT * FROM building_type')
    for line in cur.fetchall():
        print(line)
    print()

def test_building():
    print('Test building')
    cur = con.cursor()
    cur.execute('SELECT * FROM building')
    count = 0
    for line in cur.fetchall():
        print(line)
        if count > 10:
            break
        count += 1
    print()

def test_road():
    print('Test road')
    cur = con.cursor()
    cur.execute('SELECT * FROM road')
    count = 0
    for line in cur.fetchall():
        print(line)
        if count > 10:
            break
        count += 1
    print()

def test_building_position():
    print('Test building_position')
    cur = con.cursor()
    cur.execute('SELECT * FROM building_position')
    count = 0
    for line in cur.fetchall():
        print(line)
        if count > 10:
            break
        count += 1
    print()

def test_road_position():
    print('Test road_position')
    cur = con.cursor()
    cur.execute('SELECT * FROM road_position_point')
    count = 0
    for line in cur.fetchall():
        print(line)
        if count > 10:
            break
        count += 1
    print()
    cur.execute('SELECT * FROM road_position_edge')
    count = 0
    for line in cur.fetchall():
        print(line)
        if count > 10:
            break
        count += 1
    print()


if __name__ == '__main__':
    # pytest.main(['-s', 'test_db.py'])
    ...