import re


class Packet:
    def __init__(self, ptype, sender, receiver, data):
        self.ptype = ptype
        self.sender = sender
        self.receiver = receiver
        self.data = data

    def __str__(self):
        return self.ptype + " :: " + self.sender + " >> " + self.receiver + " :: " + str(self.data)


def decode_data(raw_data):
    try:
        print(raw_data)
        raw_payload = re.search("(?<=\#)(.*?)(?=\#)", raw_data.decode("utf-8"))
        raw_headers = re.search("(?<=\<)(.*?)(?=\>)", raw_data.decode("utf-8"))
        payload = raw_payload[0].split("~")
        headers = raw_headers[0].split(":")
        ptype = headers[0]
        sender = headers[1]
        receiver = headers[2]
        data = payload[2].split("-")
        pac = Packet(ptype, sender, receiver, data)
        print(pac)
        return [sender, receiver, data]
    except TypeError as et:
        print("Unable to decode payload data")
        print(et)
        return ["", "", ""]
    except Exception as e:
        print("Unable to decode payload data")
        print(e)
        return ["","",""]