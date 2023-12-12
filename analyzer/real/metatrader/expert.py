import uuid
import json


def receive_message(connection):
    data = ""
    while True:
        response = connection.recv(1)

        if not response:
            break

        # if last character is \x03, then it is the end of the message
        if response == b"\x03":
            break

        data += response.decode("utf-8")

    return json.loads(data)


class Expert:
    def __init__(self, connection) -> None:
        self.connection = connection
        pass

    def get_candles(self, symbol, timeframe="M5", n_candles=500):
        if self.connection is None:
            raise Exception("Connection not set")

        msg_id = str(uuid.uuid4())

        payload = {
            "type": "LAST_CANDLES",
            "n_candles": n_candles,
        }

        msg = {"id": msg_id, "type": "REQUEST", "payload": payload}
        msg_bytes = (json.dumps(msg) + "\x03").encode("utf-8")

        self.connection.send(msg_bytes)

        # receive message
        while True:
            data = receive_message(self.connection)

            if data["id"] != msg_id and data["type"] != "RESPONSE":
                continue

            payload = data["payload"]
            return payload
