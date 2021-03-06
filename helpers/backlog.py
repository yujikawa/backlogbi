import json
import urllib.request
import urllib.parse 
from typing import List

class BacklogAPI(object):

    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint
        self.api_key = api_key

    def get_status(self, project_id):
        url = urllib.parse.urljoin(
            self.endpoint, f'/api/v2/projects/{project_id}/statuses')
        query_params = urllib.parse.urlencode(
            {'apiKey': self.api_key,

             })
        req = urllib.request.Request('{}?{}'.format(url, query_params))
        with urllib.request.urlopen(req) as res:
            statuses = json.load(res)
        return statuses

    def get_issue_stats(self, project_id, status_list: List[int]) -> List[dict]:
        url = urllib.parse.urljoin(self.endpoint, '/api/v2/issues')
        param_list = [('statusId[]', status) for status in status_list]
        param_list += [('apiKey', self.api_key), ('projectId[]',
                                                  project_id), ('parentChild', 1), ('count', 100)]
        query_params = urllib.parse.urlencode(param_list)
        req = urllib.request.Request('{}?{}'.format(url, query_params))
        with urllib.request.urlopen(req) as res:
            issues = json.load(res)
        return issues

    def get_projects(self):
        url = urllib.parse.urljoin(self.endpoint, '/api/v2/projects')
        query_params = urllib.parse.urlencode(
            {'apiKey': self.api_key,
             })
        req = urllib.request.Request('{}?{}'.format(url, query_params))
        with urllib.request.urlopen(req) as res:
            projects = json.load(res)
        return projects

    def get_issue_stats_done(self, project_id, start_date: str, end_date: str) -> List[dict]:
        url = urllib.parse.urljoin(self.endpoint, '/api/v2/issues')
        query_params = urllib.parse.urlencode(
            {'apiKey': self.api_key,
             'updatedSince': start_date,
             'updatedUntil': end_date,
             'statusId[]': 4,
             'projectId[]': project_id,
             'parentChild': 1,
             'count': 100

             })
        req = urllib.request.Request('{}?{}'.format(url, query_params))
        with urllib.request.urlopen(req) as res:
            issues = json.load(res)
        return issues
