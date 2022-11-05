import nfc
import ndef
from threading import Thread
from nfc.clf import RemoteTarget
from nfc.tag.tt4 import Type4Tag

from command import SelectCommand
from data import Tag
from response import RAPDU
from card import Card

# def beam(llc):
#    snep_client = nfc.snep.SnepClient(llc)
#    snep_client.put_records([ndef.UriRecord('http://nfcpy.org')])


# def send_apdu(t, c):
#     # print(c.marshal())
#     data = t.send_apdu(*c.marshal(), check_status=False)
#     # print(f"{data=} {sw1=} {sw2=}")
#     # print(RAPDU.unmarshal(data))
#     if data:
#         return RAPDU.unmarshal(data)
#     return data


def connected(t):
    if isinstance(t, Type4Tag):
        # print("sending apdu")
        #
        # r = send_apdu(t, SelectCommand(b"2PAY.SYS.DDF01"))
        # # r = tag.send_apdu(0x00, 0xA4, 0x04, 0x00, b"2PAY.SYS.DDF01", 0x00)
        # print(f"{r=}")
        #
        # r2 = send_apdu(t, SelectCommand(r[Tag.AID]))
        # print(f"{r2=}")
        card = Card(t)
        # print(f"{card.get_pse()=}")

        # print(f"{card.list_applications()=}")
        print(f"{card.get_mf()=}")
        print(f"{card.get_metadata()=}")
        print(f"{card.list_applications(pse='2PAY.SYS.DDF01')=}")

        # print(f"{card.generate_cap_value('0000')=}")
    print(f"{t=}")
    return False


with nfc.ContactlessFrontend("tty") as clf:
    try:
        clf.connect(rdwr={"on-connect": connected})
    except KeyboardInterrupt:
        exit()