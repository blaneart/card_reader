import json
import logging
from textwrap import wrap
import requests
import nfc.clf.pn532
from nfc.tag.tt4 import Type4Tag

from card import Card
from command import GetDataCommand
from data import (
    Tag,
    read_tag,
    render_element,
)
from structures import TLV

logging.basicConfig(level=logging.DEBUG)
# nfc.clf.log.setLevel(logging.DEBUG)
# nfc.clf.pn532.log.setLevel(logging.DEBUG)


def parse_log_format(log_format):
    ts = []
    while log_format:
        tag, i = read_tag(log_format)
        ts.append((Tag(tag), log_format[i]))
        log_format = log_format[i + 1 :]
    return ts


def parse_logs(logs, log_format):
    ts = parse_log_format(log_format)
    result = []
    for l in logs:
        total_len = 0
        data = TLV()
        for tag, length in ts:
            total_len += length
            data[tag] = l[:length]
            l = l[length:]
        result.append(data)
        print(f"{total_len=}")

    return result


# print(parse_log_format(bytes.fromhex("9A039F21035F2A029F02069F4E149F3602")))
# print(
#     parse_logs(
#         [bytes.fromhex("00000000000653097820070700e52510030404009000")],
#         bytes.fromhex("9F27019F02065F2A029A039F36029F5206"),
#     )
# )
# exit()


def connected(t):
    if isinstance(t, Type4Tag):
        payload = {}
        card = Card(t)

        print(f"{(apps := card.list_applications())=}")
        payload["app_labels"] = [a.get(Tag.APP_LABEL) for a in apps]
        payload["app_labels"] = [a.decode("utf-8") for a in payload["app_labels"]]

        if apps:
            print(f"selecting app={apps[-1]}")
            print(f"{(app := card.select_application(list(apps[-1][Tag.ADF_NAME])))=}")

            # Language preference
            if (0x5F, 0x2D) in app.data[Tag.FCI][Tag.FCI_PROP].get(
                Tag.FCI_ISSUER_DISC, {}
            ):
                payload["languages"] = wrap(
                    app.data[Tag.FCI][Tag.FCI_PROP][Tag.FCI_ISSUER_DISC][(0x5F, 0x2D)],
                    2,
                )

            if (0x9F, 0x0A) in app.data[Tag.FCI][Tag.FCI_PROP].get(
                Tag.FCI_ISSUER_DISC, {}
            ):
                payload["card_type"] = repr(
                    app.data[Tag.FCI][Tag.FCI_PROP][Tag.FCI_ISSUER_DISC][(0x9F, 0x0A)]
                )

            if Tag.PDOL not in app.data[Tag.FCI][Tag.FCI_PROP]:
                print(f"{(processing_options := card.get_processing_options())=}")
            else:
                print(
                    f"{(processing_options := card.get_processing_options(pdol=app.data[Tag.FCI][Tag.FCI_PROP][Tag.PDOL].serialise({(0x9f, 0x66): (0x60, 0, 4, 0)})))=}"
                )

            if (0x9F, 0x36) in processing_options.data[0x77]:
                payload["transaction_counter"] = render_element(
                    (0x9F, 0x36), processing_options.data[0x77][(0x9F, 0x36)]
                )

            if (0x5F, 0x20) in processing_options.data[0x77]:
                payload["cardholder"] = processing_options.data[0x77][
                    (0x5F, 0x20)
                ].decode("utf-8")

            tag_f = None
            if Tag.RMTF1 in processing_options.data:
                tag_f = Tag.RMTF1
            elif Tag.RMTF2 in processing_options.data:
                tag_f = Tag.RMTF2

            if tag_f and Tag.AFL in processing_options.data[tag_f]:
                print(
                    f"{(app_data := card.get_application_data(processing_options.data[tag_f][Tag.AFL]))=}"
                )
                fields = {
                    "effective_date": (0x5F, 0x25),
                    "expiration_date": (0x5F, 0x24),
                    "issuer_country_code": (0x5F, 0x28),
                    "pan": 0x5A,
                    "currency": (0x9F, 0x42),
                    "currency_exp": (0x9F, 0x44),
                }
                for key, tag in fields.items():
                    if tag in app_data:
                        payload[key] = render_element(tag, app_data[tag])

            if Tag.LOG_ENTRY in app.data[Tag.FCI][Tag.FCI_PROP].get(
                Tag.FCI_ISSUER_DISC, {}
            ):
                print(
                    f"{(log_format := card.get_data_item(GetDataCommand.LOG_FORMAT,tag=Tag.LOG_FORMAT))=}"
                )
                log_sfi, log_len = app.data[Tag.FCI][Tag.FCI_PROP][Tag.FCI_ISSUER_DISC][
                    Tag.LOG_ENTRY
                ]
                logs = []
                for i in range(1, log_len + 1):
                    try:
                        l = card.read_record(i, log_sfi)
                        logs.append(l)
                    except Exception:
                        break
                print(f"{logs=}")

                # TODO
                payload["logs"] = [
                    {
                        "amount": 654,
                        "country_code": "FR",
                        "date": "20/01/01",
                        "transaction_counter": 229,
                    }
                ]

            print(f"{(metadata := card.get_metadata())=}")
            payload |= metadata

        print(payload)
        url = "http://localhost:5000/card_info"
        x = requests.post(url, json=payload)

        # print(f"{card.generate_cap_value('0000')=}")
        return False

    return False


with nfc.ContactlessFrontend("tty") as clf:
    clf.device.log.setLevel(logging.DEBUG)
    while True:
        try:
            clf.connect(rdwr={"on-connect": connected})
            from time import sleep
            sleep(5)
        except KeyboardInterrupt:
            exit()
        except Exception:
            pass