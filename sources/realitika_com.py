from site_interface import *
from bs4 import *
import requests
import datetime
import re


class RealitikaComPages(SitePages):
    def get_page(self):
        url = self.get_page_url(self._iter_page_num)
        try:
            respond = requests.get(url)

            self._soup = BeautifulSoup(respond.text, "html.parser")
            self._soup.prettify()
            # $$("div[style*='padding']")
            self._item_rows = self._soup.find_all(
                'div', attrs={'style': re.compile(r'^padding')})
            # print(self._item_rows[0])
            self._item_rows = self._item_rows[1:]

            # item = self._item_rows[0]
            # s = item.find('a', attrs={'href': re.compile(r'^http')})['href']
            # print(s)
            # print(item)
        except Exception as e:
            print(e)
            print(f'Can\t get page {url}')
            self._item_rows = []


class RealitikaCom(SiteItems):
    def get_uuid_from_url(self,
                          url: str) -> str:
        return url\
            .replace('https://www.', '')\
            .replace('hr/listing/', '')

    def get_next_item(self) -> bool:
        """ 
        return True if succesfully get new item uuid from a page,
        else return False
        """
        length_items_list = len(self._pages._item_rows)
        if (length_items_list == 0):
            return False

        # init
        self.init_data()

        # get uuid
        self._url = self._pages._item_rows[0].find(
            'a', attrs={'href': re.compile(r'^http')})['href']
        self._uuid = self.get_uuid_from_url(self._url)
        #
        price = self._pages._item_rows[0].find_all('strong')
        if len(price) > 1:
            self._price = price[1]\
                .string\
                .replace('€', '')\
                .replace('.', '')\
                .replace(',', '')\
                .strip()
        self._date = datetime.datetime.now().isoformat()
        square = self._pages._item_rows[0].find_all('div')
        if len(square) >= 3:
            square = square[2]
            self._text_lower = str(square).lower()

            has_square = False
            has_rooms = False
            has_floor = False
            for text in str(square)\
                .replace('<br>', '')\
                .replace('<sup>', '')\
                .replace('</sup>', '')\
                    .split(','):
                if not has_square:
                    i = text.find('m2')
                    if i >= 0:
                        start = i-5
                        if start < 0:
                            start = 0
                        self._square = remove_non_digit_chars(
                            text[start:i])
                        has_square = True
                if not has_rooms:
                    i = text.find('sob')
                    if i >= 0:
                        start = i-3
                        if start < 0:
                            start = 0
                        self._rooms = remove_non_digit_chars(
                            text[start:i])
                        has_rooms = True
                    if text.find('garsonjer') >= 0:
                        has_rooms = True
                if not has_floor:
                    i = text.find('sprat')
                    if i >= 0:
                        start = i-4
                        if start < 0:
                            start = 0
                        self._floor = remove_non_digit_chars(
                            text[start:i])
                        has_floor = True
                if has_square and has_rooms and has_floor:
                    break

        #
        self._pages._item_rows.pop(0)
        return True


######################
if __name__ == "__main__":

    # test
    print('Test realitika.com site for flats (for flat_rent_scraper.py): ')
    site = RealitikaCom(RealitikaComPages(
        "https://www.realitica.com/?cur_page=<page>&for=DuziNajam&opa=Podgorica&cty%5B%5D=Blok+5&cty%5B%5D=Blok+6&type%5B%5D=Home&type%5B%5D=Apartment&type%5B%5D=Room&since-day=p-anytime&lng=hr",
        '<page>'))
    for i, uuid in enumerate(site):
        print('*', i, site._url)
        print(
            f'\t €{site._price}, {site._rooms} rm, {site._square} m2, {site._floor} fl ')
        # print(f'\t {site._text}')
        print()
