import os
import json
import urllib.request
import pickle
import calendar
import datetime
import urllib
from backlogbi.models import Setting


def get_month_range(year: int, month: int) -> (str, str):
    _, last_day = calendar.monthrange(year, month)
    start_date = '{}-{:02}-{:02}'.format(year, month, 1)
    end_date = '{}-{:02}-{:02}'.format(year, month, last_day)
    return start_date, end_date


def dict_index(data: [dict], search: any):
    for i, d in enumerate(data):
        if search in d.values():
            return i
    return -1


def get_projects():
    s = Setting()
    url = urllib.parse.urljoin(s.endpoint, '/api/v2/projects')
    query_params = urllib.parse.urlencode({'apiKey': s.api_key})
    req = urllib.request.Request('{}?{}'.format(url, query_params))
    with urllib.request.urlopen(req) as res:
        projects = json.load(res)
    return projects


def get_issue_stats(start_date: str, end_date: str, project_id: str) -> dict:
    s = Setting()
    url = urllib.parse.urljoin(s.endpoint, '/api/v2/issues')
    query_params = urllib.parse.urlencode(
        {'apiKey': s.api_key, 'dueDateSince': start_date, 'dueDateUntil': end_date, 'projectId[]': project_id})
    req = urllib.request.Request('{}?{}'.format(url, query_params))
    with urllib.request.urlopen(req) as res:
        issues = json.load(res)

    result = {
        'statsInfo': {
            'dueDateSince': start_date,
            'dueDateUntil': end_date
        },
        'all': len(issues),
        'done': 0,
        'wiki': 0,
        'stars': 0,
        'byStatus': None,
        'byCategories': None,
        'actualAvgTime': 0
    }

    issue_by_category = []
    issue_by_status = []

    for issue in issues:
        # Number of issues by status
        if issue['status']['id'] == 4:
            result['done'] += 1

        dt = datetime.datetime.fromisoformat(issue['dueDate'].replace('Z', '+00:00'))
        idx = dict_index(issue_by_status, issue['status']['id'])
        if idx != -1:
            issue_by_status[idx]['count'][dt.day - 1] += 1
        else:
            temp_status = issue['status'].copy()
            temp_status['count'] = [0 for _ in range(31)]
            temp_status['count'][dt.day - 1] = 1
            issue_by_status.append(temp_status)

        # Number of issues by category
        for category in issue['category']:
            idx = dict_index(issue_by_category, category['id'])
            if idx != -1:
                issue_by_category[idx]['count'] += 1
            else:
                temp_category = category.copy()
                temp_category['count'] = 1
                del temp_category['displayOrder']
                issue_by_category.append(temp_category)

    result['byStatus'] = issue_by_status
    result['byCategories'] = issue_by_category

    return result


def get_members_stats(start_date: str, end_date: str, project_id: str) -> dict:
    s = Setting()
    url = urllib.parse.urljoin(s.endpoint, '/api/v2/issues')
    query_params = urllib.parse.urlencode(
        {'apiKey': s.api_key, 'dueDateSince': start_date, 'dueDateUntil': end_date, 'projectId[]': project_id})
    req = urllib.request.Request('{}?{}'.format(url, query_params))
    with urllib.request.urlopen(req) as res:
        issues = json.load(res)

    result = {}
    for issue in issues:
        # Number of issues by status
        if issue['assignee'] is None:
            continue

        user_id = issue['assignee']['userId']

        if user_id not in result:
            result[user_id] = {
                'userId': user_id,
                'id': issue['assignee']['id'],
                'name': issue['assignee']['name'],
                'actualAvgTime': 0,
                'all': 0,
                'done': 0,
                'byCategories': [],
                'byStatus': [],
                'wiki': 0,
                'star': 0,
            }

        result[user_id]['all'] += 1

        if issue['status']['id'] == 4:
            result[user_id]['done'] += 1

        dt = datetime.datetime.fromisoformat(issue['dueDate'].replace('Z', '+00:00'))
        idx = dict_index(result[user_id]['byStatus'], issue['status']['id'])
        if idx != -1:
            result[user_id]['byStatus'][idx]['count'][dt.day - 1] += 1
        else:
            temp_status = issue['status'].copy()
            temp_status['count'] = [0 for _ in range(31)]
            temp_status['count'][dt.day - 1] = 1
            result[user_id]['byStatus'].append(temp_status)

        # Number of issues by category
        for category in issue['category']:
            idx = dict_index(result[user_id]['byCategories'], category['id'])
            if idx != -1:
                result[user_id]['byCategories'][idx]['count'] += 1
            else:
                temp_category = category.copy()
                temp_category['count'] = 1
                del temp_category['displayOrder']
                result[user_id]['byCategories'].append(temp_category)

    return {
        'statsInfo': {
            'dueDateSince': start_date,
            'dueDateUntil': end_date
        },
        'users': [i for i in result.values()],
    }


if __name__ == '__main__':
    # 1. get issues
    d = datetime.datetime.now()
    start_date, end_date = get_month_range(d.year, d.month)
    result = get_issue_stats(start_date, end_date)
    # 2. save data
    with open('data/issues_stats.pickle', 'wb') as f:
        pickle.dump(result, f)
