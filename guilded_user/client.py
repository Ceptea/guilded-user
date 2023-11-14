"""
All the client stuff.
"""

from uuid import uuid4
import requests as req


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

    def _get(self, endpoint):
        """
        Gets the endpoint (???)
        """
        response = self.session.get(f"{API}{endpoint}")

        return response

    def _post(self, endpoint, json):
        """
        Post's to a endpoint wih the specified json
        """
        response = self.session.post(f"{API}{endpoint}", json=json)

        return response

    def _put(self, endpoint, json):
        """
        Puts to a endpoint wih the specified json
        """
        response = self.session.put(f"{API}{endpoint}", json=json)
        return response

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

    def set_presence(self, status=1):
        """
        Set's the user's presence
        """
        json = {"status": status}
        self._post("users/me/presence", json)

    def set_status(self, text, reactionid=90002547):
        """
        Set's the user's status
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

    def get_messages(self, channel, limit):
        '''
        Gets messages
        '''
        self._get(f"/channels/{channel}/messages?limit={limit}&maxReactionUsers=8")

    def send_message(
        self,
        channel,
        message,
        replies=None,
        confirmed=False,
        is_silent=False,
        is_private=False,
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
            "isSilent": is_silent,
            "isPrivate": is_private,
        }
        response = self._post(f"channels/{channel}/messages", json)
        return response
