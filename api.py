import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

URL_BASE = 'https://lucky-jet-a.1play.one'

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504, 104],
    allowed_methods=["HEAD", "POST", "PUT", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)


class Browser(object):

    def __init__(self):
        self.response = None
        self.headers = None
        self.session = requests.Session()

    def set_headers(self, headers=None):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.06"
        }
        if headers:
            for key, value in headers.items():
                self.headers[key] = value

    def get_headers(self):
        return self.headers

    def send_request(self, method, url, **kwargs):
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        return self.session.request(method, url, **kwargs)


class LuckyJetAPI(Browser):

    def __init__(self):
        super().__init__()
        self.set_headers()
        self.headers = self.get_headers()

    def get_last_crashs(self):
        self.headers = self.get_headers()
        self.headers["origin"] = f"{URL_BASE}"
        self.headers["referer"] = f"{URL_BASE}/"
        self.headers["session"] = "demo"
        self.response = self.send_request("GET",
                                          f"{URL_BASE}/public/history/api/history",
                                          headers=self.headers)
        return self.response.json()


if __name__ == '__main__':
    lja = LuckyJetAPI()
    last_crashs = lja.get_last_crashs()
    print(json.dumps(last_crashs, indent=4))


