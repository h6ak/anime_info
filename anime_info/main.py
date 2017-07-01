import argparse
from .web_scraping import AkibaSoukenInfo
from .database import DBWriter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str)
    args = parser.parse_args()

    file_name = args.f
    anime_info = AkibaSoukenInfo(file_name=file_name)
    print(anime_info.target_url)
    print(anime_info.status)
    info_list = anime_info.get()

    # TODO: DB接続情報を外部ファイルから読み込むようにする
    db_conf = {
        'host': 'localhost',
        'user': 'root',
        'database': 'anime_info'
    }

    ds = DBWriter(db_conf)
    for info in info_list:
        ds.insert_info_to_db(info)
    ds.close_db()


if __name__ == '__main__':
    main()
