import time

import requests


class LINENotifyBot:
    API_URL = "https://notify-api.line.me/api/notify"

    def __init__(self, access_token):
        self.__hearders = {"Authorization": "Bearer " + access_token}

    def send(
        self,
        message,
        image=None,
    ):
        payload = {
            "message": message,
        }

        files = {}
        if image != None:
            files = {"imageFile": open(image, "rb")}

        print("------ send line message ------")
        r = requests.post(
            LINENotifyBot.API_URL,
            headers=self.__hearders,
            data=payload,
            files=files,
        )
        print(r)
        time.sleep(1)
        print("------ finished ------")
