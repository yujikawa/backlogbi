from flask import Flask, jsonify, request
from flask_cors import CORS
import analyze
import datetime

api = Flask(__name__)
CORS(api)


@api.route('/healthy', methods=['GET'])
def healthy():
    return jsonify({'message': 'success'})


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


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8080)
