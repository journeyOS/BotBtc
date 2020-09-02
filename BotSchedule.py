#  !/usr/bin/env python
#  -*- encoding: utf-8 -*-
#
#  Copyright (c) 2020 anqi.huang@outlook.com
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import threading
import time

import requests
import schedule as schedule

from im.dingding import DingDing

from base import Utils

message = "### [ETH]({eth_url}) = {eth_price}\n" \
          "### [BTC]({btc_url}) = {btc_price}"

url = 'http://api.huobi.br.com/market/history/kline?symbol={who}'

userConfig = Utils.readUserConfig()
bot_key_test = userConfig["bot"]["bot_key_test"]
access_token = userConfig["dingding"]["access_token"]
secret = userConfig["dingding"]["secret"]


def runThreaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def jobFetch():
    ethusdt_url = url.format(who='ethusdt')
    ethusdt = requests.post(ethusdt_url)
    eth = ethusdt.json()['data'][0]['close']
    print(eth)
    btcusdt_url = url.format(who='btcusdt')
    btcusdt = requests.post(btcusdt_url)
    btc = btcusdt.json()['data'][0]['close']
    print(btc)

    ding = DingDing(access_token)
    ding.set_secret(secret)
    ding.send_markdown('BTC和ETH', message.format(eth_url=ethusdt_url, eth_price=eth,
                                                 btc_url=btcusdt_url, btc_price=btc))


schedule.every(1).minutes.do(runThreaded, jobFetch)

if __name__ == '__main__':
    jobFetch()
    while True:
        schedule.run_pending()
        time.sleep(1)
