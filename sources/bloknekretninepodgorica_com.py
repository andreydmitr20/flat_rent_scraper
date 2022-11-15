from site_interface import *
from bs4 import *
import requests
import datetime
import re


class BloknekretninepodgoricaComPages(SitePages):
    def get_page(self):
        url = self.get_page_url(self._iter_page_num + 1)

        # debug
        # print(f'\n{url}\n')
        # if self._iter_page_num==1:
        #     self._item_rows =[]
        #     return

        try:
            respond = requests.get(url)

            self._soup = BeautifulSoup(respond.text, "html.parser")
            self._soup.prettify()
            # $$("div[style*='padding']")
            self._item_rows = self._soup.find_all(
                'div', attrs={'class': re.compile(r'^property')})
            # print(self._item_rows[0])
            # self._item_rows = self._item_rows[1:]

            # item = self._item_rows[0]
            # s = item.find('a', attrs={'href': re.compile(r'^http')})['href']
            # print(s)
            # print(item)
        except Exception as e:
            print(e)
            print(f'Can\t get page {url}')
            self._item_rows = []


class BloknekretninepodgoricaCom(SiteItems):
    def get_uuid_from_url(self,
                          url: str) -> str:
        return url \
            .replace('https://www.', '') \
            .replace('property/izdavanje-', '')

    def get_next_item(self) -> bool:
        """ 
        return True if succesfully get new item uuid from a page,
        else return False
        """
        while (True):
            length_items_list = len(self._pages._item_rows)
            if (length_items_list == 0):
                return False

            # init
            self.init_data()

            # get uuid
            url = self._pages._item_rows[0].find(
                'a', attrs={'href': re.compile(r'^http')})['href']

            # if it is not rent
            is_rent = url.find('izdavanje') >= 0 and find_any_keyword(url, [
                'stan',
                'garsonjera',
                'kuca',
            ])
            if (not is_rent) or find_any_keyword(url, [
                'prostor',
                'stomatoloska-ordinacija',
                'kancelarija'
            ]):
                self._pages._item_rows.pop(0)
                continue

            self._url = url
            # uuid
            self._uuid = self.get_uuid_from_url(self._url)

            div = self._pages._item_rows[0].find_all('div')
            # price
            try:
                this_price = self._pages._item_rows[0].find('a', attrs={'class': re.compile(r'^price')}).string
                price = remove_non_digit_chars(this_price)
            except Exception as e:
                price='0'

            self._price = price

            # date
            self._date = datetime.datetime.now().isoformat()

            text = (str(self._pages._item_rows[0]
                        .find('div', attrs={'class': re.compile(r'^title-block')})) +
                    str(self._pages._item_rows[0]
                        .find('div', attrs={'class': re.compile(r'^entry')}))).lower()

            self._text_lower = text

            # floor
            i = text.find('sprat')
            if i >= 0:
                start = i - 5
                if start < 0:
                    start = 0
                self._floor = get_roman_number_to_50(text[start:i])

            # square
            i = url.find('m2')
            if i >= 0:
                start = i - 3
                if start < 0:
                    start = 0
                self._square = remove_non_digit_chars(url[start:i])
            if url.find('jednosoban') >= 0:
                self._rooms = 1
            if url.find('dvosoban') >= 0:
                self._rooms = 2
            if url.find('trosoban') >= 0:
                self._rooms = 3
            if url.find('cetvorosoban') >= 0:
                self._rooms = 4
            # if url.find('dvosoban')>=0:
            #     self._rooms=5
            if url.find('garsonjera') >= 0:
                self._rooms = 0

            # exit from while
            break

        #
        self._pages._item_rows.pop(0)
        return True


######################
if __name__ == "__main__":

    # test
    print('Test bloknekretninepodgoric.com site for flats (for flat_rent_scraper.py): ')
    site = BloknekretninepodgoricaCom(BloknekretninepodgoricaComPages(
        "https://www.bloknekretninepodgorica.com/location/podgorica/page/<page>/",
        '<page>'))
    for i, uuid in enumerate(site):
        print('*', i, site._url)
        print(f'\t €{site._price}, {site._square} m2, {site._rooms} r,')
        print(site._text_lower)
        # print(f'\t €{site._price}, {site._rooms} rm, {site._square} m2, {site._floor} fl ')
        # print(f'\t {site._text}')
        print()
