from db_connection import get_db_connection 
from cities_info import cities, connections

def insert_city(city_name, latitude, longitude):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("Insert INTO Cities (city_name, latitude, longitude) VALUES (%s, %s, %s)", 
                (city_name, latitude, longitude))
    conn.commit()
    cur.close()
    conn.close()

def insert_connection(start_city, end_city, distance):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Connections (start_city_id, end_city_id, distance) 
        VALUES (
                (SELECT city_id FROM Cities WHERE city_name = %s),
                (SELECT city_id FROM Cities WHERE city_name = %s),
                %s) """, 
                (start_city, end_city, distance)) 
    conn.commit()
    cur.close()
    conn.close()

# Insert the cities together with their latitude and longitude
for city, latitude, longitude in cities:
    insert_city(city, latitude, longitude)

# Insert all connections/edges 
for start_city, end_city, distance in connections:
    insert_connection(start_city, end_city, distance)


