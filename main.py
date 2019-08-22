# coding: utf-8

import time
from datetime import datetime, timedelta, timezone
from requests_html import HTMLSession
from slack_webhooks import SlackWebhooks

def notice_upcoming_contests(last_updated, now):
    contests = []
    for contest in get_upcoming_contests():
        notification_time = contest['start_time'] - timedelta(seconds=60*60*3)
        if last_updated < notification_time and notification_time < now:
            contests += contest

    if not contests:
        return

    slack = SlackWebhooks()
    message = "予定されたコンテスト\n"
    for i, contest in enumerate(contests):
        days = ["(月)", "(火)", "(水)", "(木)", "(金)", "(土)", "(日)"]
        message = "{}{} {}\n".format(
                contest['start_time'].strftime("%m/%d"),
                days[contest['start_time'].weekday()],
                contest['contest_name'])

    print(message)
    payload = {"text" : message}
    slack.post(payload)

def get_upcoming_contests():
    session = HTMLSession()
    r = session.get('https://atcoder.jp/contests/?lang=ja')
    sel = '#contest-table-upcoming > div > div > table > tbody'
    upcoming_contests = r.html.find(sel, first=True).find('tr')
    ret = []
    for contest in upcoming_contests:
        contest = contest.find('td')
        dic = {}
        dic['start_time'] = datetime.strptime(contest[0].text, '%Y-%m-%d %H:%M:%S%z')
        dic['contest_name'] = contest[1].text
        dic['screen_name'] = list(contest[1].links)[0].split('/')[-1]
        dic['link'] = list(contest[1].absolute_links)[0]
        [hour, minute] = map(int, contest[2].text.split(':'))
        dic['duration'] = ((hour * 60) + minute) * 60
        dic['rated_range'] = contest[3].text
        ret.append(dic)
    return ret

def main():
    interval = 60 * 60
    last_updated = datetime.now(timezone(timedelta(seconds=9*60*60)))
    while True:
        now = datetime.now(timezone(timedelta(seconds=9*60*60)))
        notice_upcoming_contests(last_updated, now)

        time.sleep(interval)
        last_updated = datetime.now()

if __name__ == '__main__':
    main()

