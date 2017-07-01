import datetime as dt
import mysql.connector as sql


class DBWriter(object):
    def __init__(self, db_conf):
        self._conn = sql.connect(**db_conf)

    def close_db(self):
        self._conn.close()

    def write_info_to_db(self, info: dict) -> None:
        title = info['title']
        if title is None:
            return

        official_site = info['official_site']
        aid = self._write_anime(title, official_site)

        schedule = info['schedule']
        if len(schedule) <= 0:
            self._conn.commit()
            return

        for sch in schedule:
            station = sch['station']
            onair = sch['onair']

            sid = self._write_station(station)
            self._write_onair(aid, sid, onair)

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

    def _exist_onair(self, aid: int, sid: int) -> bool:
        query = (
            'SELECT id FROM first_onair_informations '
            'WHERE animation_id = %s AND station_id = %s '
            'LIMIT 1'
        )
        cur = self._conn.cursor()
        cur.execute(query, (aid, sid))
        cur.fetchall()
        rowcount = cur.rowcount
        cur.close()

        if rowcount > 0:
            return True

        return False

    def _write_anime(self, title, official_site) -> int:
        # auto_increment の値をむやみに増やさないようにするため、ON DUPLICATE KEY UPDATEを行わない
        cur = self._conn.cursor()

        aid = self._find_animation_id(title)
        if aid:
            query = (
                'UPDATE animations '
                'SET official_site = %(site)s '
                'WHERE id = %(aid)s'
            )

            cur.execute(query, {'aid': aid, 'site': official_site})
            cur.close()

            return aid

        query = (
            'INSERT INTO animations '
            '(title, official_site) '
            'VALUES (%s, %s)'
        )
        cur.execute(query, (title, official_site))
        cur.close()

        return self._find_animation_id(title)

    def _write_station(self, name: str) -> int:
        # auto_increment の値をむやみに増やさないようにするため、ON DUPLICATE KEY UPDATEを行わない
        sid = self._find_station_id(name)
        if sid:
            return sid

        query = 'INSERT INTO stations (name) VALUES (%s)'
        cur = self._conn.cursor()
        cur.execute(query, (name, ))
        cur.close()

        return self._find_station_id(name)

    def _write_onair(self, aid: int, sid: int, start_at: dt.datetime) -> None:
        # auto_increment の値をむやみに増やさないようにするため、ON DUPLICATE KEY UPDATEを行わない
        cur = self._conn.cursor()

        if self._exist_onair(aid, sid):
            query = (
                'UPDATE first_onair_informations '
                'SET start_at = %(start_at)s '
                'WHERE animation_id = %(aid)s AND station_id=%(sid)s'
            )
            cur.execute(query, {'aid': aid, 'sid': sid, 'start_at': start_at})
        else:
            query = (
                'INSERT INTO first_onair_informations '
                '(animation_id, station_id, start_at) '
                'VALUES (%s, %s, %s)'
            )
            cur.execute(query, (aid, sid, start_at))

        cur.close()
