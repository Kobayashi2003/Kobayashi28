import sqlite3
import json

# TABLE
# campus(int:campus_id(PK), text:campus_name, text:campus_addr, text:campus_area, text:campus_info, int:postal_code)
# building_type(building_type_id(PK), building_type_name)
# building(building_id(PK), building_name, building_number, building_type_id(FK), building_info, campus_id(FK))
# building_position(building_id(PK), x, y, width, height, map_width, map_height)
# road(road_id(PK), road_name, road_number, road_info, campus_id(FK))
# road_position_point(point_id(PK), road_id, point_x, point_y, point_radius, point_info)
# road_position_edge(edge_id(PK), road_id, point_id_1(FK), point_id_2(FK), edge_info)

def get_db():
    return sqlite3.connect('school_map.db')


def init_db(con: sqlite3.Connection):
    with open('origin/schema.sql') as f:
        command = f.read().replace('AUTO_INCREMENT', 'AUTOINCREMENT')
        con.executescript(command)


def load_data_campus(con: sqlite3.Connection):
    cur = con.cursor()
    with open('origin/campus.txt', encoding='utf-8') as f: # campus_id campus_name address postal_code area
        # throw away the first line
        f.readline()
        for line in f:
            line = line.strip().split()
            # move the "" around the elements
            line = [element.strip('"') for element in line]
            campus_id, campus_name, campus_addr, postal_code, campus_area = line
            cur.execute('INSERT INTO campus (campus_id, campus_name, campus_addr, postal_code, campus_area) VALUES (?, ?, ?, ?, ?)', 
                        (campus_id, campus_name, campus_addr, postal_code, campus_area))
    con.commit()


def load_data_building_type(con: sqlite3.Connection):
    cur = con.cursor()
    with open('origin/building_type.txt', encoding='utf-8') as f: # building_type_id building_type_name
        # throw away the first line
        f.readline()
        for line in f:
            line = line.strip().split()
            # move the "" around the elements
            line = [element.strip('"') for element in line]
            building_type_id, building_type = line
            cur.execute('INSERT INTO building_type (building_type_id, building_type) VALUES (?, ?)', 
                        (building_type_id, building_type))
    con.commit()


def load_data_building(con: sqlite3.Connection):
    cur = con.cursor()
    with open('origin/build.json', encoding='utf-8') as f: # build_id build_name number type campus_id
        data = json.load(f)
        data = data['RECORDS']
        for build in data:
            build_id = build['build_id']
            build_name = build['build_name']
            build_number = build['number']
            build_type = build['type']
            building_type_id = cur.execute('SELECT building_type_id FROM building_type WHERE building_type = ?',(build_type,)).fetchone()[0]
            campus_id = build['campus_id']
            cur.execute('INSERT INTO building (building_id, building_name, building_number, building_type_id, campus_id) VALUES (?, ?, ?, ?, ?)',
                        (build_id, build_name, build_number, building_type_id, campus_id))
    con.commit()


def load_data_building_position(con: sqlite3.Connection):
    cur = con.cursor()
    # no data, just generate it
    import random
    for i in range(1, 100):
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        width = random.randint(1, 100)
        height = random.randint(1, 100)
        map_width = random.randint(1, 100)
        map_height = random.randint(1, 100)
        cur.execute('INSERT INTO building_position (building_id, x, y, width, height, map_width, map_height) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (i, x, y, width, height, map_width, map_height))
    con.commit()


def load_data_road(con: sqlite3.Connection):
    cur = con.cursor()
    with open('origin/road.json', encoding='utf-8') as f: # road_id road_name campus_id
        data = json.load(f)
        data = data['RECORDS']
        for road in data:
            road_id = road['road_id']
            road_name = road['road_name']
            campus_id = road['campus_id']
            cur.execute('INSERT INTO road (road_id, road_name, campus_id) VALUES (?, ?, ?)',
                        (road_id, road_name, campus_id))
    con.commit()


def load_data_road_position_point(con: sqlite3.Connection):
    cur = con.cursor()
    # no data, just generate it
    import random
    for i in range(1, 100):
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        radius = random.randint(1, 100)
        cur.execute('INSERT INTO road_position_point (point_id, road_id, point_x, point_y, point_radius) VALUES (?, ?, ?, ?, ?)',
                    (i, 1, x, y, radius))
    con.commit()


def load_data_road_position_edge(con: sqlite3.Connection):
    cur = con.cursor()
    # no data, just generate it
    import random
    for i in range(1, 100):
        point_id_1 = random.randint(1, 50)
        point_id_2 = random.randint(1, 50)
        if point_id_1 == point_id_2:
            continue
        cur.execute('INSERT INTO road_position_edge (edge_id, road_id, point_id_1, point_id_2) VALUES (?, ?, ?, ?)',
                    (i, 1, point_id_1, point_id_2))
    con.commit()


def close_db(con: sqlite3.Connection):
    con.close()



def create_json_campus():

    import os
    if not os.path.exists('data'):
        os.mkdir('data')

    con = get_db()
    cur = con.cursor()
    json_data = {}
    RECODES = []
    # campus
    cur.execute('SELECT * FROM campus')
    campus = cur.fetchall()
    for line in campus:
        c = {}
        c['campus_id'] = line[0]
        c['campus_name'] = line[1]
        c['campus_addr'] = line[2]
        c['campus_area'] = line[3]
        c['campus_info'] = line[4]
        c['postal_code'] = line[5]
        RECODES.append(c)
    json_data['RECODES'] = RECODES

    with open('data/campus.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    con.close()


def create_json_building_type():
    
    import os
    if not os.path.exists('data'):
        os.mkdir('data')

    con = get_db()
    cur = con.cursor()
    json_data = {}
    RECODES = []
    # building_type
    cur.execute('SELECT * FROM building_type')
    building_type = cur.fetchall()
    for line in building_type:
        b = {}
        b['building_type_id'] = line[0]
        b['building_type'] = line[1]
        RECODES.append(b)
    json_data['RECODES'] = RECODES

    with open('data/building_type.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    con.close()


def create_json_building():
    import os
    if not os.path.exists('data'):
        os.mkdir('data')

    con = get_db()
    cur = con.cursor()
    json_data = {}
    RECODES = []
    # building
    cur.execute('SELECT * FROM building')
    building = cur.fetchall()
    for line in building:
        b = {}
        b['building_id'] = line[0]
        b['building_name'] = line[1]
        b['building_number'] = line[2]
        b['building_type_id'] = line[3]
        b['building_info'] = line[4]
        b['campus_id'] = line[5]
        RECODES.append(b)
    json_data['RECODES'] = RECODES

    with open('data/building.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    con.close()


def create_json_road():
    import os
    if not os.path.exists('data'):
        os.mkdir('data')

    con = get_db()
    cur = con.cursor()
    json_data = {}
    RECODES = []
    # road
    cur.execute('SELECT * FROM road')
    road = cur.fetchall()
    for line in road:
        r = {}
        r['road_id'] = line[0]
        r['road_name'] = line[1]
        r['road_number'] = line[2]
        r['road_info'] = line[3]
        r['campus_id'] = line[4]
        RECODES.append(r)
    json_data['RECODES'] = RECODES

    with open('data/road.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    con.close()


def create_json_building_position():
    import os
    if not os.path.exists('data'):
        os.mkdir('data')

    con = get_db()
    cur = con.cursor()
    json_data = {}
    RECODES = []
    # building_position
    cur.execute('SELECT * FROM building_position')
    building_position = cur.fetchall()
    for line in building_position:
        b = {}
        b['building_id'] = line[0]
        b['x'] = line[1]
        b['y'] = line[2]
        b['width'] = line[3]
        b['height'] = line[4]
        b['map_width'] = line[5]
        b['map_height'] = line[6]
        RECODES.append(b)
    json_data['RECODES'] = RECODES

    with open('data/building_position.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    con.close()


def create_json_road_position_point():
    import os
    if not os.path.exists('data'):
        os.mkdir('data')

    con = get_db()
    cur = con.cursor()
    json_data = {}
    RECODES = []
    # road_position_point
    cur.execute('SELECT * FROM road_position_point')
    road_position_point = cur.fetchall()
    for line in road_position_point:
        r = {}
        r['point_id'] = line[0]
        r['road_id'] = line[1]
        r['point_x'] = line[2]
        r['point_y'] = line[3]
        r['point_radius'] = line[4]
        r['point_info'] = line[5]
        RECODES.append(r)
    json_data['RECODES'] = RECODES

    with open('data/road_position_point.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    con.close()


def create_json_road_position_edge():
    import os
    if not os.path.exists('data'):
        os.mkdir('data')

    con = get_db()
    cur = con.cursor()
    json_data = {}
    RECODES = []
    # road_position_edge
    cur.execute('SELECT * FROM road_position_edge')
    road_position_edge = cur.fetchall()
    for line in road_position_edge:
        r = {}
        r['edge_id'] = line[0]
        r['road_id'] = line[1]
        r['point_id_1'] = line[2]
        r['point_id_2'] = line[3]
        r['edge_info'] = line[4]
        RECODES.append(r)
    json_data['RECODES'] = RECODES

    with open('data/road_position_edge.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    con.close()


def create_json():
    create_json_campus()
    create_json_building_type()
    create_json_building()
    create_json_road()
    create_json_building_position()
    create_json_road_position_point()
    create_json_road_position_edge()


if __name__ == '__main__':
    # db = get_db()
    # init_db(db)
    # load_data_campus(db)
    # load_data_building_type(db)
    # load_data_building(db)
    # load_data_road(db)
    # load_data_building_position(db)
    # load_data_road_position_point(db)
    # load_data_road_position_edge(db)
    # close_db(db)
    create_json()