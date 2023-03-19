from typing import Literal


def load_file(file_name: str):
    with open(file_name, 'r') as file:
        for line in file:
            yield line


def cmd_filter(data, query: str):
    return filter(lambda data: query in data, data)


def cmd_map(data, col_number):
    return (item.split(' ')[0] for item in data)


def cmd_sort(data, order_by: Literal['asc', 'desc']):
    return sorted(data, reverse=True if order_by == 'desc' else False)


def cmd_limit(data, limit: int):
    return (item[0] for item in zip(data, range(limit), strict=False))


def cmd_unique(data):
    return set(data)


if __name__ == "__main__":
    file_data = load_file('data/apache_logs_small.txt')
    data = cmd_filter(file_data, '7')
    data = cmd_map(data, 0)
    data = cmd_sort(data, 'desc')
    data = cmd_limit(data, 4)
    data = cmd_unique(data)
    print(list(data))
