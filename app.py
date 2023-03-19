import os
from typing import Literal

from flask import Flask, abort, request

app = Flask(__name__)


def load_file(file_name: str):
    with open(file_name, 'r') as file:
        for line in file:
            yield line


def cmd_filter(data, query: str):
    return filter(lambda data: query in data, data)


def cmd_map(data, col_number):
    return (item.split(' ')[col_number] for item in data)


def cmd_sort(data, order_by: Literal['asc', 'desc']):
    return sorted(data, reverse=True if order_by == 'desc' else False)


def cmd_limit(data, limit: int):
    return (item[0] for item in zip(data, range(limit), strict=False))


def cmd_unique(data):
    return set(data)


def make_cmd(cmd: str, data, param: str):
    match cmd:
        case 'filter': return cmd_filter(data, param)
        case 'map': return cmd_map(data, int(param))
        case 'sort': return cmd_sort(data, param)
        case 'limit': return cmd_limit(data, int(param))
        case 'unique': return cmd_unique(data)


@app.route('/perform_query', methods=['POST', 'GET'])
def perform_query():
    if request.method == 'POST':
        params = request.json
    elif request.method == 'GET':
        params = request.args

    cmd1 = params.get('cmd1')
    value1 = params.get('value1')
    cmd2 = params.get('cmd2')
    value2 = params.get('value2')
    filename = params.get('filename')

    if not os.path.exists(f'data/{filename}'):
        return abort(400)

    if (cmd1 or cmd2) not in ('filter', 'map', 'sort', 'limit', 'unique'):
        return abort(400)

    data = make_cmd(cmd1, load_file(f'data/{filename}'), value1)
    data = make_cmd(cmd2, data, value2)

    return app.response_class('\n'.join(data), content_type="text/plain")


@app.errorhandler(400)
def problem_w_file(e):
    return "С запросом ерунда какая-то", 400


if __name__ == "__main__":
    app.run()
