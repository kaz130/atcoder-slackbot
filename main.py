# coding: utf-8

from datetime import datetime, timedelta, timezone
from requests_html import HTMLSession
from slack_webhooks import SlackWebhooks

def main():
    post_upcoming_contests()

def post_upcoming_contests():
    slack = SlackWebhooks()
    contests = get_upcoming_contests()
    message = "予定されたコンテスト\n"
    for i, contest in enumerate(contests):
        days = ["(月)", "(火)", "(水)", "(木)", "(金)", "(土)", "(日)"]
        message += contest['start_time'].strftime("%m/%d") \
        + days[contest['start_time'].weekday()] \
        + " " + contest['contest_name']
        if (i != len(contests) - 1):
            message += "\n"

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

if __name__ == '__main__':
    main()

