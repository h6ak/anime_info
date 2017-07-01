import argparse
from .web_scraping import AkibaSoukenInfo
from .data_storage import DataStorage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str)
    args = parser.parse_args()

    file_name = args.f
    anime_info = AkibaSoukenInfo(file_name=file_name)
    info_list = anime_info.get()

    ds = DataStorage()

    for info in info_list:
        ds.insert_info_to_db(info)


if __name__ == '__main__':
    main()
