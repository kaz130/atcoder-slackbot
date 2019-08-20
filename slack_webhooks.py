# coding: utf-8

import requests
import json
import config

class SlackWebhooks:
    def __init__(self):
        self.webhook_url = config.WEBHOOK_URL

    def post(self, payload, color=None):
        requests.post(self.webhook_url, data = json.dumps(payload))

