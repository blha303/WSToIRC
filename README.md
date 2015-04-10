# WSToIRC

I wanted a thing to feed [Reddit live threads](https://reddit.com/r/live) to an IRC channel, figured I'd use my [SingleMessageBot](https://gist.github.com/blha303/e3cf2d93c932a082c5eb) module to save time. This project also introduced me to Tornado, which is pretty darn fantastic.

### Caveats
* At the moment this is designed specifically for reddit live threads, allowing users to pass a live thread url by argument and retrieving the websocket url from that. Other uses can be allowed for by simply modifying main() in wstoirc.py.

### Usage
* Clone the repo
* `pip install -r requirements.txt`
* Run the script once to generate irc settings: `python wstoirc.py`
* Edit smbotconfig.json
* Run the script again: `python wstoirc.py [reddit live thread url]`. If no url is provided it defaults to [my test thread](https://www.reddit.com/live/upqxckdrqrl4)
