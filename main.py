# coding: utf-8

import time
from datetime import datetime, timedelta, timezone
from requests_html import HTMLSession
from slack_webhooks import SlackWebhooks
import logging
import click

logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def notice(contests, message):
    if not contests:
        return

    slack = SlackWebhooks()
    for i, contest in enumerate(contests):
        days = ["(月)", "(火)", "(水)", "(木)", "(金)", "(土)", "(日)"]
        message = "{}{} {}\n".format(
                contest['start_time'].strftime("%m/%d"),
                days[contest['start_time'].weekday()],
                contest['contest_name'])

    payload = {"text" : message}
    logger.debug("notice:" + payload)
    slack.post(payload)

def get_contests(contest_type):
    session = HTMLSession()
    r = session.get('https://atcoder.jp/contests/?lang=ja')
    selectors = {
            "action" : '#contest-table-action > div > div > table > tbody',
            "permanent" : '#contest-table-permanent > div > div > table > tbody',
            "upcoming" : '#contest-table-upcoming > div > div > table > tbody',
            "recent" : '#contest-table-recent > div > div > table > tbody'
            }
    sel = selectors[contest_type]

    contests = r.html.find(sel, first=True).find('tr')
    ret = []
    for contest in contests:
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
        logger.debug("get_contest:" + dic['screen_name'])
    return ret

@click.command()
@click.argument('notice_time', default=12)
def main(notice_time):
    now = datetime.now(timezone(timedelta(seconds=9*60*60)))

    notice_contests = []
    for contest in get_contests("upcoming"):
        if contest['start_time'] < now + timedelta(hours=notice_time):
            notice_contests.append(contest)

    notice(notice_contests, "予定されたコンテスト")

if __name__ == '__main__':
    main()

