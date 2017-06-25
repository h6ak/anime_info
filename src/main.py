import requests
from bs4 import BeautifulSoup


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


def main():
    anime_info = AnimeInfo(file_name='sample.html')
    info = anime_info.get()

    for i in info:
        print(i)
        print('\n')


if __name__ == '__main__':
    main()
