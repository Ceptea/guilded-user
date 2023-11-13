"""
All the client stuff.
"""


import requests as req
from uuid import uuid4

API = "https://www.guilded.gg/api/"


class ApiError(Exception):
    """
    A api error occurred.
    """


class Client:
    """
    Guilded Client
    """

    def __init__(self) -> None:
        self.session = req.Session()

    def _post(self, endpoint, json):
        """
        Post's to a endpoint wih the specified json
        """
        response = self.session.post(f"{API}{endpoint}", json=json)

        return response

    def _put(self, endpoint, json):
        """
        Put's to a endpoint wih the specified json
        """
        response = self.session.put(f"{API}{endpoint}", json=json)
        return response

    def login(self, email, password, get_me=True):
        """
        Logins to a guilded account with the specified creds
        """

        json = {
            "email": email,
            "password": password,
            "getMe": get_me,
        }
        response = self._post("login", json)
        if response.status_code != 200:
            raise ApiError("Invaild Login.")
        return response.json()

    def _ping(self):
        """
        Not sure what this does.
        Just added it cause I saw guilded doing it alot.
        will probably be removed
        """
        response = self._put("users/me/ping", {})
        if response.status_code != 200:
            raise ApiError(f"Tried to ping but got {response.status_code}")
        return response

    def set_status(self, text, reactionid=90002547):
        """
        Set's your status
        """
        json = {
            "content": {
                "object": "value",
                "document": {
                    "object": "document",
                    "data": {},
                    "nodes": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "data": {},
                            "nodes": [
                                {
                                    "object": "text",
                                    "leaves": [
                                        {"object": "leaf", "text": text, "marks": []}
                                    ],
                                }
                            ],
                        }
                    ],
                },
            },
            "customReactionId": reactionid,
            "expireInMs": 0,
        }
        response = self._post("users/me/status", json)
        return response

    def send_message(
        self,
        channel,
        message,
        replies=None,
        confirmed=False,
        is_Silent=False,
        is_Private=False,
    ):
        """
        Sends a message to the specified channel
        """
        if not replies:
            replies = []
        json = {
            "messageId": str(uuid4()),
            "content": {
                "object": "value",
                "document": {
                    "object": "document",
                    "data": {},
                    "nodes": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "data": {},
                            "nodes": [
                                {
                                    "object": "text",
                                    "leaves": [
                                        {
                                            "object": "leaf",
                                            "text": message,
                                            "marks": [],
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                },
            },
            "repliesToIds": replies,
            "confirmed": confirmed,
            "isSilent": is_Silent,
            "isPrivate": is_Private,
        }
        response = self._post(f"channels/{channel}/messages", json)
        return response
