# coding: utf-8

import datetime
from requests_html import HTMLSession

def main():
    pass

def get_upcoming_contests():
    session = HTMLSession()
    r = session.get('https://atcoder.jp/contests/?lang=ja')
    sel = '#contest-table-upcoming > div > div > table > tbody'
    upcoming_contests = r.html.find(sel, first=True).find('tr')
    ret = []
    for contest in upcoming_contests:
        contest = contest.find('td')
        contest = [element.text for element in contest]
        dic = {}
        dic['start_time'] = datetime.datetime.strptime(contest[0], '%Y-%m-%d %H:%M:%S%z')
        dic['contest_name'] = contest[1]
        [hour, minute] = map(int, contest[2].split(':'))
        dic['duration'] = ((hour * 60) + minute) * 60
        dic['rated_range'] = contest[3]
        ret.append(dic)
    return ret

if __name__ == '__main__':
    main()

