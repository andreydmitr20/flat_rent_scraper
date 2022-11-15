import json

import requests
import datetime


class TelegramBot():
    def __init__(self):
        self.__private_info = self.load_private_info()

    def load_private_info(self):
        try:
            with open('private_info.json', 'r') as json_file:
                return json.loads(json_file.read())
        except Exception as e:
            print(e)
            return {}

    # send file
    def send_file_to_telegram(self,
                              file_name: str,
                              do_send=False) -> None:
        if not do_send:
            return
        try:

            with open(file_name, 'r') as file:
                url = f"https://api.telegram.org/bot{self.__private_info['bot_token']}/sendDocument"
                # print(
                requests.post(url, data={'chat_id': self.__private_info['chat_id']}, files={'document': file})
                # )
        except Exception as e:
            print(e)
            print('Can\'t send file to Telegram.')

        # send to telegram

    def send_message_to_telegram(self,
                                 message: str,
                                 do_send=False) -> None:
        if not do_send:
            return
        try:

            url = f"https://api.telegram.org/bot{self.__private_info['bot_token']}/sendMessage?chat_id={self.__private_info['chat_id']}&text={message}"
            # print(
            requests.get(url).json()
            # )
        except Exception as e:
            print(e)
            print('Can\'t send message to Telegram.')


####################
if __name__ == "__main__":
    # send_file_to_telegram(
    #     '/media/hdd/KURSUVODUPROGRAMIRANJE/MY/MY_SCRAPER/site_interface.py',
    #     1)
    # send_message_to_telegram('bot test', 1)
    tlg=TelegramBot()
    tlg.send_message_to_telegram(datetime.datetime.strftime(
        datetime.datetime.now(), '%Y-%m-%d No new items'
    ), 1)
