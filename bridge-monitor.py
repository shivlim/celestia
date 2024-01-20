from systemd import journal
from datetime import datetime, timedelta
from time import sleep
import telegram
import requests


TELEGRAM_TOKEN      = ''
CHAT_ID             = ''




bot=telegram.Bot(token=TELEGRAM_TOKEN)

def record_status(msg):
    # sending a telgram message
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    print(requests.get(url).json()) # this sends the message


if __name__ == "__main__":
    lastheight = "N/A"
    while True:
        try:
             j = journal.Reader()
             j.this_boot()
             j.seek_realtime(datetime.now() - timedelta(seconds=60))
             j.log_level(journal.LOG_INFO)
             j.add_match(_SYSTEMD_UNIT="celestia-bridge.service")

             for entry in j:
                m = entry['MESSAGE']
                if('new head' in m):
                    height = m[m.find("\"height\":"):m.find("\"hash\":")]
                    print(height)
                    currentheight = height
             if lastheight != "N/A" :
                 print('lastheight is ' + lastheight)
                 print('currentheight is ' + currentheight)
                 if lastheight == currentheight :
                     record_status("BRIDGE NOT MOVING")
                     print('something wrong..height not moving')
             print('setting lastheight height to' + currentheight)
             lastheight = currentheight
             sleep(60)
        except Exception as e:
            print(e)
