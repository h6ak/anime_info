import re
import datetime as dt
import requests
from bs4 import BeautifulSoup


class AkibaSoukenInfo(object):
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
        """
        Get animation information
        :return: A list of dictionaries.
            Each dictionary has information of one animation.
        """
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
            return str(m_title.a.string)
        return None

    @staticmethod
    def _official_site(item_box: BeautifulSoup) -> [str, None]:
        official = item_box.find('div', {'class': 'official'})
        if official:
            official_site = official.find('a', {'class': 'officialSite'})
            if official_site:
                return official_site.get('href')

        return None

    def _schedule(self, item_box: BeautifulSoup) -> [None]:
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

                info['station'] = str(station.string) if station else None

                if onair and onair.string:
                    onair_date_str = str(onair.string)
                    info['onair'] = self.parse_datetime(onair_date_str)
                else:
                    info['onair'] = None

                result.append(info)

        return result

    @staticmethod
    def parse_datetime(date_str: str) -> [dt.datetime, None]:
        """
        Parse string like '2017年7月3日(月)25:35～' to datetime
        :param date_str: string
        :return: datetime
        """
        reg_ex = re.compile(r'[0-9]+')
        datetime_elms = reg_ex.findall(date_str)
        datetime_elms = [int(elm) for elm in datetime_elms]

        # TODO; 情報が不足しているものをどうするか
        if len(datetime_elms) < 5:
            return None

        year = datetime_elms[0]
        month = datetime_elms[1]
        day = datetime_elms[2]
        hour = datetime_elms[3]
        minute = datetime_elms[4]

        parsed_datetime = dt.datetime(year=year, month=month, day=day)
        if hour and minute:
            parsed_datetime += dt.timedelta(hours=hour, minutes=minute)

        return parsed_datetime
