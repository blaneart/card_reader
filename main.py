import logging

import nfc.clf.pn532
from nfc.tag.tt4 import Type4Tag

from card import Card
from data import Tag

logging.basicConfig(level=logging.DEBUG)
# nfc.clf.log.setLevel(logging.DEBUG)
# nfc.clf.pn532.log.setLevel(logging.DEBUG)

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
        # r = t.send_apdu(
        #     0x00, 0xA4, 0x04, 0x00, b"2PAY.SYS.DDF01", 0x00, check_status=False
        # )

        # r = t.send_apdu(
        #     0x00, 0xA4, 0x04, 0x00, b"2PAY.SYS.DDF01", 0x00, check_status=True
        # )

        # print(f"{r=}")
        # return
        #
        # r2 = send_apdu(t, SelectCommand(r[Tag.AID]))
        # print(f"{r2=}")
        card = Card(t)
        # print(f"{card.get_pse('2PAY.SYS.DDF01')=}")
        # return

        # print(f"{card.list_applications()=}")
        # print(f"{card.get_mf()=}")
        # print(f"{card.get_metadata()=}")

        # card = Card(t)
        print(f"{(apps := card.list_applications())=}")
        # print(f"{(apps := card.list_applications('1PAY.SYS.DDF01'))=}")
        if apps:
            print(f"selecting app={apps[-1]}")
            print(f"{(app := card.select_application(list(apps[-1][Tag.ADF_NAME])))=}")
            if Tag.PDOL not in app.data[Tag.FCI][Tag.FCI_PROP]:
                print(f"{(processing_options := card.get_processing_options())=}")
            else:
                print(
                    f"{(processing_options := card.get_processing_options(pdol=app.data[Tag.FCI][Tag.FCI_PROP][Tag.PDOL].serialise({(0x9f, 0x66): (0x60, 0, 4, 0)})))=}"
                )

            tag_f = None
            if Tag.RMTF1 in processing_options.data:
                tag_f = Tag.RMTF1
            elif Tag.RMTF2 in processing_options.data:
                tag_f = Tag.RMTF2

            if tag_f and Tag.AFL in processing_options.data[tag_f]:
                print(
                    f"{(app_data := card.get_application_data(processing_options.data[tag_f][Tag.AFL]))=}"
                )

        # print(f"{card.generate_cap_value('0000')=}")
    print(f"{t=}")
    return False


with nfc.ContactlessFrontend("tty") as clf:
    clf.device.log.setLevel(logging.DEBUG)
    try:
        clf.connect(rdwr={"on-connect": connected})
    except KeyboardInterrupt:
        exit()
