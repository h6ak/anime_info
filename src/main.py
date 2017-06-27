import requests
from bs4 import BeautifulSoup
import mysql.connector as sql


class AnimeInfo(object):
    target_url = None
    html_text = None
    _item_boxes = None

    def __init__(self, file_name=None):
        if file_name:
            self._set_html_text_from_file(file_name)
        else:
            self._set_target_url()
            self._set_html_text_from_web()

        soup = BeautifulSoup(self.html_text, 'lxml')
        self._item_boxes = soup.findAll('div', {'class': 'itemBox'})

    def get(self):
        result = []
        for ib in self._item_boxes:
            info = {}

            info['title'] = self._title(ib)
            info['official_site'] = self._official_site(ib)
            info['schedule'] = self._schedule(ib)

            result.append(info)

        return result

    def _set_target_url(self) -> None:
        # TODO: 時期によってtarget_urlを変更したい
        self.target_url = 'https://akiba-souken.com/anime/summer/'

    def _set_html_text_from_web(self) -> None:
        response = requests.get(self.target_url)
        print('STATUS: {0}'.format(response.status_code))
        self.html_text = response.text

    def _set_html_text_from_file(self, file_name: str) -> None:
        with open(file_name, 'rt') as f:
            self.html_text = f.read()

    @staticmethod
    def _title(item_box: BeautifulSoup) -> [str, None]:
        m_title = item_box.find('div', {'class': 'mTitle'})
        if m_title and m_title.a:
            return m_title.a.string
        return None

    @staticmethod
    def _official_site(item_box: BeautifulSoup) -> [str, None]:
        official = item_box.find('div', {'class': 'official'})
        if official:
            official_site = official.find('a', {'class': 'officialSite'})
            if official_site:
                return official_site.get('href')

        return None

    @staticmethod
    def _schedule(item_box: BeautifulSoup) -> [None]:
        result = []
        schedule = item_box.find('div', {'class': 'schedule'})
        if schedule:
            td_list = schedule.findAll('td')
            for td in td_list:
                info = {}

                station = td.find('span', {'class': 'station'})
                onair = td.find('span', {'class': ''})

                if station is None and onair is None:
                    continue

                info['station'] = station.string if station else None
                info['onair'] = onair.string if onair else None

                result.append(info)

        return result


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
    anime_info = AnimeInfo(file_name='sample.html')
    info_list = anime_info.get()

    for info in info_list:
        insert_info_to_db(info)
        #print(info)
        #print('\n')
        #break


if __name__ == '__main__':
    main()
