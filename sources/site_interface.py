
# TODO check page load was ok

class SitePages():
    def __init__(self,
                 page_url_with_pattern: str,
                 page_num_pattern: str) -> None:
        self.__page_url_with_pattern = page_url_with_pattern
        self.__page_num_pattern = page_num_pattern

        self._iter_page_num = 0
        self._soup = None
        self._last_page = False
        self._item_rows = None

    def get_page_url(self, page_num: int) -> str:
        return self.__page_url_with_pattern.replace(
            self.__page_num_pattern, str(page_num))

    def iter_stop(self):
        """ to stop iterator externally """
        self._last_page = True

    def __iter__(self):
        self._iter_page_num = 0
        self._last_page = False
        self.get_page()
        return self

    def __next__(self) -> int:
        """
        do not know when will be last page,
        call iter_stop
        """
        if self._last_page:
            raise StopIteration
        else:
            self._iter_page_num += 1
            self.get_page()
            return self._iter_page_num


class SiteItems():
    def __init__(self,
                 scraper_pages: SitePages) -> None:
        self._pages = scraper_pages
        self._item = None
        self.init_data()

    def get_item_dict(self) -> dict:
        """ return data dict for current object :
        {...data...} """

        return {
            'uuid': self._uuid,
            'text_lower': self._text_lower,
            'price': self._price,
            'url': self._url,
            'square': self._square,
            'address': self._address,
            'date': self._date,
            'floor': self._floor,
            'rooms': self._rooms,
            'delete': self._delete,
            'days_on_site':self._days_on_site
        }

    def init_data(self) -> None:
        self._uuid = ''
        self._text_lower = ''
        self._price = '0'
        self._url = ''
        self._square = '0'
        self._address = ''
        self._date = ''
        self._floor = '0'
        self._rooms = '0'
        self._delete = False
        self._days_on_site='0'
    def get_next_item(self) -> bool:
        """ 
        return True if succesfully get new item uuid from a page,
        else return False
        """

        pass

    def __iter__(self):
        self._iter_item_num = 0
        self._pages.__iter__()
        return self

    def __next__(self) -> int:
        last_item = False
        if not self.get_next_item():
            # try next page
            self._pages.__next__()
            last_item = not self.get_next_item()

        if last_item:
            self._pages.iter_stop()
            raise StopIteration
        else:
            self._iter_item_num += 1
            return self._uuid
            # return self._iter_item_num


def remove_non_digit_chars(inp_str: str) -> str:
    """ return '0' if no digits, 
    else return only digits from string"""

    ret_str = ''
    for ch in inp_str:
        if ch >= '0' and ch <= '9':
            ret_str += ch
    if ret_str == '':
        return '0'
    return ret_str


def find_any_keyword(text: str, key_list: list) -> bool:
    for key in key_list:
        if text.find(key) >= 0:
            return True
    return False


def find_all_keyword(text: str, key_list: list) -> bool:
    for key in key_list:
        if text.find(key) < 0:
            return False
    return True


def get_roman_number_to_50(inp_str: str) -> str:
    """ return '0' if no roman numbers, 
    else return roman number < 50 as arabic number string"""
    ret_str = ''
    for ch in inp_str:
        if ch == 'i' or ch == 'v' or ch == 'x':
            ret_str += ch
    if ret_str == '':
        return '0'

    roman = {'i': 1, 'v': 5, 'x': 10}
    res = 0
    i = 0
    n = len(ret_str)
    while (i < n):
        s1 = roman[ret_str[i]]
        if (i + 1 < n):
            s2 = roman[ret_str[i+1]]
            if (s1 >= s2):
                res += s1
                i += 1
            else:
                res += s2 - s1
                i += 2
        else:
            res += s1
            i += 1

    return str(res)





######################
if __name__ == "__main__":
    print(get_roman_number_to_50('ix'))
    print(get_roman_number_to_50('i'))
    print(get_roman_number_to_50('vi'))
    print(get_roman_number_to_50('iv'))
    print(get_roman_number_to_50('xvi'))
