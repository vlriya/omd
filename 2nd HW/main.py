from typing import Dict, List
import csv

DATA_PATH = 'data/Corp_Summary.csv'
OUTPUT_PATH = 'output/result.csv'

Row = Dict[str, str]
Rows = List[Row]


def read_csv(path: str = DATA_PATH, delimiter: str = ';') -> Rows:
    """
    Читает данные в формате CSV и форматирует их в список словарей.

    :param path: путь к CSV-файлу (по умолчанию в папке data)
    :param delimiter: разделитель столбцов (по умолчанию ';')
    :return: список строк-словарей по заголовкам таблицы CSV
    """
    with open(path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return [row for row in reader]


def print_department_hierarchy(rows: Rows) -> None:
    """
    Выводит таблицу-иерархию департаментов по отделам.

    :param rows: данные из CSV
    :return: None
    """
    tree: Dict[str, set] = {}
    for r in rows:
        dept = (r.get('Департамент') or '').strip()
        team = (r.get('Отдел') or '').strip()
        if not dept or not team:
            continue
        tree.setdefault(dept, set()).add(team)

    if not tree:
        print('Данные не найдены.')
        return

    for dept in sorted(tree):
        print(f'- {dept}')
        for team in sorted(tree[dept]):
            print(f'  • {team}')


def print_summary_report(rows: Rows) -> List[Dict[str, str]]:
    """
    Выводит сводный отчет по департаментам.

    Наполнение сводного отчета:
      - department - департамент
      - number_of_employees - численность
      - min_salary - минимальная зарплата
      - max_salary - максимальная зарплата
      - avg_salary - средняя зарплата

    :param rows: данные из CSV
    :return: список словарей с данными сводного отчета
    """
    buckets: Dict[str, List[float]] = {}
    for r in rows:
        dept = (r.get('Департамент') or '').strip()
        raw = (r.get('Оклад') or '').strip().replace(' ', '')
        if not dept or not raw:
            continue
        try:
            salary = float(raw.replace(',', '.'))
        except ValueError:
            continue
        buckets.setdefault(dept, []).append(salary)

    summary_report: List[Dict[str, str]] = []
    for dept in sorted(buckets):
        salaries = buckets[dept]
        if not salaries:
            continue
        summary_report.append({
            'department': dept,
            'number_of_employees': str(len(salaries)),
            'min_salary': f'{min(salaries):.0f}',
            'max_salary': f'{max(salaries):.0f}',
            'avg_salary': f'{(sum(salaries) / len(salaries)):.0f}',
        })

    if not summary_report:
        print('Данные не найдены.')
        return summary_report

    header = (
        'department',
        'number_of_employees',
        'min_salary',
        'max_salary',
        'avg_salary'
    )
    widths = {
        h: max(
            len(h),
            *(len(r[h]) for r in summary_report)
        )
        for h in header
    }
    print(' | '.join(h.center(widths[h]) for h in header))
    print('-' * (sum(widths.values()) + 3 * (len(header) - 1)))
    for row in summary_report:
        print(' | '.join(row[h].center(widths[h]) for h in header))

    return summary_report


def save_summary_report(rows: Rows, path: str = OUTPUT_PATH) -> None:
    """
    Сохраняет сводный отчет в формате CSV (по умолчанию разделитель ';').

    :param rows: данные из CSV
    :param path: путь к результирующему файлу (по умолчанию в папке output)
    """
    summary_report = print_summary_report(rows)
    fieldnames = (
        'department',
        'number_of_employees',
        'min_salary',
        'max_salary',
        'avg_salary'
    )
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for row in summary_report:
            writer.writerow(row)
    print(f'Сводный отчёт сохранён в: {path}')


def main() -> None:
    try:
        rows = read_csv(DATA_PATH)
    except FileNotFoundError:
        print(f'Файл не найден: {DATA_PATH}')
        return

    option = ''
    options = {
        '1': 'Вывести иерархию департаментов',
        '2': 'Вывести сводный отчет по департаментам',
        '3': 'Сохранить сводный отчёт в CSV',
    }
    while option not in options:
        print(
            'Выберите из следующих вариантов:\n'
            + '\n'.join(f'{k}) {v}' for k, v in options.items())
        )
        option = input().strip()

    if option == '1':
        print_department_hierarchy(rows)
    elif option == '2':
        print_summary_report(rows)
    elif option == '3':
        save_summary_report(rows, OUTPUT_PATH)


if __name__ == '__main__':
    main()
