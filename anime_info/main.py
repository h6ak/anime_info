import argparse
import mysql.connector as sql
from .web_scraping import AkibaSoukenInfo


def insert_info_to_db(info: dict) -> None:
    db_conf = {'host': 'localhost', 'user': 'root', 'database': 'anime_info'}
    conn = sql.connect(**db_conf)

    insert_anime(conn, info)
    aid = find_animation_id(conn, str(info['title']))

    schedule = info['schedule']
    for sch in schedule:
        station = str(sch['station'])
        insert_station(conn, station)
        sid = find_station_id(conn, station)

        #print(aid, sid)

    conn.commit()
    conn.close()


def insert_anime(conn, info: dict) -> None:
    title = str(info['title'])
    official_site = str(info.get('official_site'))
    query = (
        'INSERT IGNORE INTO animations (title, official_site) '
        'VALUES (%s, %s) '
        'ON DUPLICATE KEY UPDATE '
        'official_site = VALUES(official_site)'
    )
    cur = conn.cursor()
    cur.execute(query, (title, official_site))
    cur.close()


def insert_station(conn, name: str) -> None:
    query = 'INSERT IGNORE INTO stations (name) VALUES (%s)'
    cur = conn.cursor()
    cur.execute(query, (name, ))
    cur.close()


def find_animation_id(conn, title):
    query_finc_aid = 'SELECT id FROM animations WHERE title = %s'
    cur = conn.cursor(dictionary=True)
    cur.execute(query_finc_aid, (title, ))
    fecth_result = cur.fetchall()
    aid = fecth_result[0]['id'] if cur.rowcount > 0 else None
    cur.close()

    return aid


def find_station_id(conn, station):
    query_finc_sid = 'SELECT id FROM stations WHERE name = %s'
    cur = conn.cursor(dictionary=True)
    cur.execute(query_finc_sid, (station, ))
    fecth_result = cur.fetchall()
    sid = fecth_result[0]['id'] if cur.rowcount > 0 else None
    cur.close()

    return sid


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str)
    args = parser.parse_args()

    file_name = args.f
    anime_info = AkibaSoukenInfo(file_name=file_name)
    info_list = anime_info.get()

    for info in info_list:
        insert_info_to_db(info)
        #print(info)
        #print('\n')

if __name__ == '__main__':
    main()
