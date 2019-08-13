import json
import os
from collections import namedtuple

import requests

BASE_URL = "https://api.imgur.com/{resource}"

Account = namedtuple("Account", "id,username")


class ImgurClient:
    def __init__(self, client_id=None, client_secret=None, refresh_token=None):
        self.client_id = client_id or os.getenv("IMGUR_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("IMGUR_CLIENT_SECRET")
        self.refresh_token = refresh_token or os.getenv("IMGUR_REFRESH_TOKEN")
        self.account = None
        self.access_token = None

    def _auth_headers(self, **extras):
        authed_header = {"Authorization": f"Bearer {self.access_token}"}
        authed_header.update(extras)
        return authed_header

    def fill_access_token(self):
        url = BASE_URL.format(resource="oauth2/token")
        data = {
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
        }
        result = requests.post(
            url,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        parsed_result = json.loads(result.text)
        if result.status_code == 200:
            self.access_token = parsed_result["access_token"]
            self.account = Account(
                parsed_result["account_id"], parsed_result["account_username"]
            )
        else:
            raise Exception(parsed_result["data"]["error"])

    def get_user(self, username):
        username = username or self.account.username
        url = BASE_URL.format(resource=f"3/account/{username}")

        result = requests.get(url, headers=self._auth_headers())
        if result.ok:
            return json.loads(result.text)["data"]
        return None

    def get_albums(self, username=None):
        username = username or self.account.username
        url = BASE_URL.format(resource=f"3/account/{username}/albums/")
        response = requests.get(url, headers=self._auth_headers())

        return json.loads(response.text)["data"]

    def create_album(self, title, description):
        url = BASE_URL.format(resource="3/album")
        data = {"title": title, "description": description}
        response = requests.post(
            url,
            data=data,
            headers=self._auth_headers(
                **{"Content-Type": "application/x-www-form-urlencoded"}
            ),
        )

        if response.ok:
            return True
        return False

    def upload_image(self, image_path, title=None, description=None, album=None):
        url = BASE_URL.format(resource="3/upload")
        with open(image_path, "rb") as bfile:
            response = requests.post(
                url, files={"image": bfile}, data={}, headers=self._auth_headers()
            )
            json_response = json.loads(response.text)
            if response.ok:
                return json_response["data"]["id"]
            return None
