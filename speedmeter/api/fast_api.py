import re
import requests


class FastSpeedTest:
    BASE_URL = "https://fast.com"
    API_URL = "https://api.fast.com/netflix/speedtest/v2"

    def __init__(self):
        self.token = self._get_fast_token()

    def _get_fast_token(self):
        response = requests.get(self.BASE_URL)
        response.raise_for_status()

        script_names = re.findall("app-.*\\.js", response.text)[:1]
        if not script_names:
            raise RuntimeError("Script name not found.")

        script_url = f"{self.BASE_URL}/{script_names[0]}"
        script_response = requests.get(script_url)
        script_response.raise_for_status()

        token_match = re.search(r'token:"([a-zA-Z0-9]+)"', script_response.text)
        if not token_match:
            raise RuntimeError("Token not found.")

        return token_match.group(1)

    def get_dl_urls(self, url_count):
        params = {"https": "true", "token": self.token, "urlCount": url_count}
        response = requests.get(self.API_URL, params=params)
        response.raise_for_status()

        re_urls = response.json()
        client = re_urls.get("client", {})

        return [url.get("url") for url in re_urls.get("targets", [])], client

