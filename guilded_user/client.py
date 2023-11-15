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


#


class Client:
    """
    Guilded Client
    """

    def __init__(self) -> None:
        self.session = req.Session()
        self.id = None
        self.name = None
        self.info = None

    def _get(self, endpoint):
        """
        Gets the endpoint (???)
        """
        response = self.session.get(f"{API}{endpoint}")

        return response

    def _post(self, endpoint, json):
        """
        Posts to a endpoint wih the specified json
        """
        response = self.session.post(f"{API}{endpoint}", json=json)

        return response

    def _put(self, endpoint, json):
        """
        Puts to a endpoint wih the specified json
        """
        response = self.session.put(f"{API}{endpoint}", json=json)
        return response

    def _delete(self, endpoint):
        response = self.session.delete(f"{API}{endpoint}")
        return response

    def _ping(self):
        """
        Not sure what this does.
        Just added it cause I saw guilded doing it alot.
        will probably be removed
        """
        response = self._put("users/me/ping", {})
        if response.status_code != 200:
            print(response.text)
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
        json = response.json()
        self.id = json["user"]["id"]
        self.name = json["user"]["name"]
        self.info = json
        return json

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
        """
        Gets messages
        """
        response = self._get(
            f"/channels/{channel}/messages?limit={limit}&maxReactionUsers=8"
        )
        return response.json()

    def get_channels(self):
        response = self._get(f"users/{self.id}/channels")
        if response.status_code != 200:
            raise ApiError("Failed to get channels.")
        return response.json()

    def delete_message(self, channel, message):
        response = self._delete(f"channels/{channel}/messages/{message}")
        if response.status_code != 200:
            raise ApiError("Failed to delete message. (Does it exist?)")

    def edit_message(self, channel, message, text):
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
            }
        }
        response = self._put(f"channels/{channel}/messages/{message}", json)
        if response.status_code != 200:
            print(response.text)

            raise ApiError("Failed to edit message")
        return response

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
        uuid = str(uuid4())
        json = {
            "messageId": uuid,
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
        if response.status_code != 200:
            print(response.text)
            print(response.headers)
            raise ApiError("Failed to send message")
        return Message(self, uuid, channel)


class Message:
    def __init__(self, client, uuid, channel) -> None:
        self.client = client
        self.uuid = uuid
        self.channel = channel

    def edit(self, text):
        self.client.edit_message(self.channel, self.uuid, text)

    def delete(self):
        self.client.delete_message(self.channel, self.uuid)


#
