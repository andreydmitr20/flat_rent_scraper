from realitika_com import *
from bloknekretninepodgorica_com import *
from send_to_telegram import *

import os
import csv


class FlatRentScraper():
    """ Collect a flat rent data from web sites.
    Parameters:
    - data_path : path to a .scv rent flat data file;
    - is_item_good : criteria function (is_item_good(item: dict) -> bool);
    - list_of_siteitems : list of SiteItems objects.
    """

    def __init__(self,
                 data_path: str,
                 list_of_siteitems: list) -> None:
        self.__data_path = data_path
        self.__data_file_name = data_path + 'scraper.csv'
        self.__list_of_siteitems = list_of_siteitems
        self.__data_dict = {}
        self.__delimiter = ','
        self.__quotechar = '"'
        self.__fieldnames = []
        self.__tlg = TelegramBot()
        self.__criteria = self.load_criteria()
        self.run()

    def load_criteria(self):
        try:
            with open('criteria.json', 'r') as json_file:
                # print(json_file.read())
                return json.loads(json_file.read())
        except Exception as e:
            print(e)
            return {}

    def run(self) -> None:
        try:

            if len(self.__list_of_siteitems) > 0:
                self.__fieldnames = list(self.__list_of_siteitems[0]
                                         .get_item_dict().keys())
                self.load_data()

                number_of_new_good_items = 0

                for site in self.__list_of_siteitems:

                    for i, uuid in enumerate(site):
                        print('.', end='')
                        if uuid not in self.__data_dict.keys():
                            # check item params
                            item_dict = site.get_item_dict()

                            # apply criteria
                            if self.is_item_good(item_dict):
                                number_of_new_good_items += 1

                                self.__data_dict[uuid] = item_dict
                                # print(i, site._url)

                                # check if too much new good items
                                if number_of_new_good_items < 3:
                                    # send a good item to a messenger
                                    self.__tlg.send_message_to_telegram(
                                        f'€{site._price},{site._rooms}r,{site._square}m2,{site._floor}f ' +
                                        site._url, 1)

                        else:
                            # mark item as actual
                            self.__data_dict[uuid]['delete'] = False

                if number_of_new_good_items > 0:
                    self.save_data()
                    if number_of_new_good_items > 2:
                        # send file
                        self.__tlg.send_file_to_telegram(self.__data_file_name, 1)
                else:
                    self.__tlg.send_message_to_telegram(datetime.datetime.strftime(
                        datetime.datetime.now(), '%Y-%m-%d No new items'
                    ), 1)
        except Exception as e:
            print(e)
            self.__tlg.send_message_to_telegram(datetime.datetime.strftime(
                datetime.datetime.now(), '%Y-%m-%d Fix me please'
            ), 1)
    def load_data(self) -> bool:
        """ load database"""
        try:
            self.__data_dict = {}
            # current date
            date_now = datetime.datetime.date(
                datetime.datetime.now())
            with open(self.__data_file_name, 'r') as csv_file:
                dict_reader = csv.DictReader(csv_file,
                                             delimiter=self.__delimiter,
                                             quotechar=self.__quotechar)
                for row_dict in dict_reader:
                    uuid = row_dict['uuid']
                    row_dict.pop('uuid')
                    row_dict['delete'] = True
                    date = datetime.datetime.date(
                        datetime.datetime.fromisoformat(row_dict['date']))
                    days_on_site = abs((date_now - date).days)
                    row_dict['days_on_site'] = str(days_on_site)
                    self.__data_dict[uuid] = row_dict
                return True
        except Exception as e:
            print(e)

            return False

    def save_data(self) -> bool:
        def sorter(x):
            return x[1]['date']

        try:
            data_file_name_tmp = self.__data_file_name + '.tmp'
            with open(data_file_name_tmp, 'w') as csv_file:
                dict_writer = csv.DictWriter(csv_file,
                                             fieldnames=self.__fieldnames,
                                             delimiter=self.__delimiter,
                                             quotechar=self.__quotechar)
                dict_writer.writeheader()

                # for key in self.__data_dict.keys():
                for key, row in sorted(self.__data_dict.items(),
                                       key=sorter,
                                       reverse=True):

                    # row = self.__data_dict[key]

                    if row['delete'] != True or \
                            int(row['days_on_site']) < 31:
                        row['uuid'] = key
                        row['text_lower'] = ''

                        dict_writer.writerow(row)

            # remove old data file
            try:
                os.remove(self.__data_file_name)
            except Exception as e:
                print(e)
            # rename tmp data file to current data file
            try:
                os.rename(data_file_name_tmp, self.__data_file_name)
            except Exception as e:
                print(e)
            return True
        except Exception as e:
            print(e)
            return False

    # criteria
    def is_item_good(self,
                     item: dict) -> bool:
        square = int(item.get('square', '0'))
        price = int(item.get('price', '0'))
        floor = int(item.get('floor', '0'))
        rooms = int(item.get('rooms', '0'))
        text_lower = item.get('text_lower', '')
        result = (square == 0 or square >= self.__criteria["square greate or equal"]) and \
                 price <= self.__criteria["price less or equal"] and \
                 (floor == 0 or floor <= self.__criteria["floor less or equal"]) and \
                 (rooms >= self.__criteria["rooms greate or equal"]) and \
                 find_any_keyword(text_lower, self.__criteria["find any keyword"])
        if result:
            print(
                f"\n*** {item['url']}")
            print(
                f"€{item['price']} rm:{item['rooms']} {item['square']}m2 fl:{item['floor']}")
        return result


#####################
if __name__ == "__main__":
    # sleep_time_in_seconds = 4*60*60
    # while (True):

    print('\nA flat rent scraper is running.')
    FlatRentScraper(
        '',  # '/media/hdd/scraper/',
        list_of_siteitems=[

            RealitikaCom(
                RealitikaComPages(
                    "https://www.realitica.com/?cur_page=<page>&for=DuziNajam&opa=Podgorica&cty%5B%5D=Blok+5&cty%5B%5D=Blok+6&type%5B%5D=Home&type%5B%5D=Apartment&type%5B%5D=Room&since-day=p-anytime&lng=hr",
                    '<page>')
            ),

            BloknekretninepodgoricaCom(
                BloknekretninepodgoricaComPages(
                    "https://www.bloknekretninepodgorica.com/location/podgorica/page/<page>/",
                    '<page>')
            ),

        ])

    # print(f'\nNow the scraper is sleeping {sleep_time_in_seconds} seconds.')
    # time.sleep(sleep_time_in_seconds)
