import datetime
import json

from flask import jsonify, request
from backlogbi import api
from backlogbi.models import Setting
from backlogbi import analyze


@api.route('/healthy', methods=['GET'])
def healthy():
    return jsonify({'message': 'success'})


@api.route('/v1/settings', methods=['GET'])
def get_settings():
    s = Setting()
    return jsonify({'endpoint': s.endpoint, 'apiKey': s.api_key})


@api.route('/v1/settings', methods=['POST', 'PUT'])
def create_settings():
    data = request.data.decode('utf-8')
    data = json.loads(data)
    s = Setting()
    result = s.set_option(data['endpoint'], data['apiKey'])
    if result:
        return jsonify({'endpoint': s.endpoint, 'apiKey': s.api_key})
    else:
        return jsonify({'endpoint': '', 'apiKey': ''})


@api.route('/v1/projects', methods=['GET'])
def get_projects():
    result = analyze.get_projects()
    return jsonify(result)


@api.route('/v1/stats/issues', methods=['GET'])
def get_issues():
    yyyymm = request.args.get('yyyymm')
    project_id = request.args.get('projectId')

    if project_id is None:
        return jsonify({'errors': ['Please set project ID in query parameter']})

    start_date = None;
    end_date = None;

    if yyyymm is None:
        d = datetime.datetime.now()
        start_date, end_date = analyze.get_month_range(d.year, d.month)
    else:
        year, month = yyyymm.split('-')
        start_date, end_date = analyze.get_month_range(int(year), int(month))

    result = analyze.get_issue_stats(start_date, end_date, project_id)

    return jsonify(result)


@api.route('/v1/stats/members', methods=['GET'])
def get_members():
    yyyymm = request.args.get('yyyymm')
    project_id = request.args.get('projectId')
    if project_id is None:
        return jsonify({'errors': ['Please set project ID in query parameter']})
    start_date = None;
    end_date = None;

    if yyyymm is None:
        d = datetime.datetime.now()
        start_date, end_date = analyze.get_month_range(d.year, d.month)
    else:
        year, month = yyyymm.split('-')
        start_date, end_date = analyze.get_month_range(int(year), int(month))

    result = analyze.get_members_stats(start_date, end_date, project_id)

    return jsonify(result)
