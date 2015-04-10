from tornado import gen
from tornado.websocket import websocket_connect
from tornado.ioloop import IOLoop
from singlemessagebot import SingleMessageBot
from json import loads
from sys import argv
import requests

viewcount = (0, False) # count, is_fuzzed
items = {} # LiveUpdate_guid: data

def on_message(message, url):
    def shorten(url):
        return requests.get("http://is.gd/create.php", params={'format': 'simple', 'url': url}).text
    type, payload = loads(message).values()
    msg = None
    if type == "activity":
        global viewcount
        viewcount = payload.values()
    elif type == "update":
        payload = payload["data"]
        payload["link"] = shorten(url + u"/updates/" + payload["id"])
        items[payload["name"]] = payload
        msg = u"\x0315{link}\x0f /u/{author}: {body}".format(**payload) + (u" (has embeds)" if payload["embeds"] else u"")
    elif type == "strike":
        item = items[payload] if payload in items else None
        if item:
            msg = u"\x034STRICKEN\x0f: \x0315{link} /u/{author}: {body}".format(**item)
        else:
            msg = u"Unlogged update \x034stricken\x0f! " + shorten(url + u"/updates/" + payload[11:])
    print(type)
    print(payload)
    if msg:
        print(msg)
        bot = SingleMessageBot(msg)
        bot.start()

@gen.coroutine
def main(url, pageurl):
    ws = yield websocket_connect(wsurl)
    while True:
        msg = yield ws.read_message()
        if msg is None:
            break
        on_message(msg, pageurl)

if __name__ == "__main__":
    url = argv[1] if len(argv) > 1 else "https://www.reddit.com/live/upqxckdrqrl4"
    wsurl = requests.get(url + "/about.json",
                         headers={"User-Agent": "live thread tests by /u/suudo"}
                         ).json()["data"]["websocket_url"].replace("&amp;", "&")
    main(wsurl, url)
    IOLoop.instance().start()

