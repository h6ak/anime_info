import datetime as dt
import mysql.connector as sql


class DataStorage(object):
    def __init__(self):
        db_conf = {'host': 'localhost', 'user': 'root', 'database': 'anime_info'}
        self._conn = sql.connect(**db_conf)

    def close_db(self):
        self._conn.close()

    def insert_info_to_db(self, info: dict) -> None:
        title = info['title']
        if title is None:
            return

        official_site = info['official_site']
        aid = self._insert_anime(title, official_site)

        schedule = info['schedule']
        if len(schedule) <= 0:
            return

        for sch in schedule:
            station = sch['station']
            onair = sch['onair']

            sid = self._insert_station(station)
            self._insert_onair(aid, sid, onair)

        self._conn.commit()

    def _find_animation_id(self, title: str) -> int:
        query_finc_aid = 'SELECT id FROM animations WHERE title = %s'
        cur = self._conn.cursor(dictionary=True)
        cur.execute(query_finc_aid, (title, ))

        fetch_result = cur.fetchall()
        aid = int(fetch_result[0]['id']) if cur.rowcount > 0 else None
        cur.close()

        return aid

    def _find_station_id(self, station: str) -> int:
        query_finc_sid = 'SELECT id FROM stations WHERE name = %s'
        cur = self._conn.cursor(dictionary=True)
        cur.execute(query_finc_sid, (station, ))

        fetch_result = cur.fetchall()
        sid = int(fetch_result[0]['id']) if cur.rowcount > 0 else None
        cur.close()

        return sid

    def _insert_anime(self, title, official_site) -> int:
        query = (
            'INSERT INTO animations '
            '(title, official_site) '
            'VALUES (%s, %s) '
            'ON DUPLICATE KEY UPDATE '
            'official_site = VALUES(official_site)'
        )
        cur = self._conn.cursor()
        cur.execute(query, (title, official_site))
        cur.close()

        return self._find_animation_id(title)

    def _insert_station(self, name: str) -> int:
        query = 'INSERT IGNORE INTO stations (name) VALUES (%s)'
        cur = self._conn.cursor()
        cur.execute(query, (name, ))
        cur.close()

        return self._find_station_id(name)

    def _insert_onair(self, aid: int, sid: int, start_at: dt.datetime) -> None:
        query = (
            'INSERT INTO first_onair_informations '
            '(animation_id, station_id, start_at) '
            'VALUES (%s, %s, %s) '
            'ON DUPLICATE KEY UPDATE '
            'start_at = VALUES(start_at)'
        )
        cur = self._conn.cursor()
        cur.execute(query, (aid, sid, start_at))
        cur.close()
