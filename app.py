import os
import re
from typing import Generator, Iterable, Iterator

from flask import Flask, Response, abort, request

app = Flask(__name__)


def load_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name, 'r') as file:
        for line in file:
            yield line


def cmd_filter(data: Iterator[str], query: str) -> Iterator[str]:
    return filter(lambda data: query in data, data)


def cmd_map(data: Iterator[str], col_number: int) -> Iterator[str]:
    return (item.split(' ')[col_number] for item in data)


def cmd_sort(data: Iterator[str], order_by: str) -> list[str]:
    return sorted(data, reverse=True if order_by == 'desc' else False)


def cmd_limit(data: Iterator[str], limit: int) -> Iterator[str]:
    return (item[0] for item in zip(data, range(limit), strict=False))


def cmd_unique(data: Iterator[str]) -> list[str]:
    return list(set(data))


def cmd_regex(data: Iterator[str], rstring: str) -> Iterator[str]:
    for item in data:
        smth = re.search(rstring, item)
        if smth:
            yield item


def make_cmd(data: Iterator[str], cmd: str, param: str) -> Iterable[str]:
    match cmd:
        case 'filter': return cmd_filter(data, param)
        case 'map': return cmd_map(data, int(param))
        case 'sort': return cmd_sort(data, param)
        case 'limit': return cmd_limit(data, int(param))
        case 'unique': return cmd_unique(data)
        case 'regex': return cmd_regex(data, param)


@app.route('/perform_query', methods=['POST', 'GET'])
def perform_query() -> Response:
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

    if cmd1 not in ('filter', 'map', 'sort', 'limit', 'unique', 'regex'):
        return abort(400)
    else:
        data = make_cmd(load_file(f'data/{filename}'), cmd1, value1)
        if cmd2 in ('filter', 'map', 'sort', 'limit', 'unique', 'regex'):
            data = make_cmd(data, cmd2, value2)

    return app.response_class('\n'.join(data), content_type="text/plain")


@app.errorhandler(400)
def problem_w_file(e):
    return "С запросом ерунда какая-то", 400


if __name__ == "__main__":
    app.run()
