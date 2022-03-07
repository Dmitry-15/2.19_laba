#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import argparse
import os.path
import pathlib


def add_human(people, name, zodiac, year):
    """
    Добавить данные о человеке.
    """
    people.append(
        {
            'name': name,
            'zodiac': zodiac,
            'year': year,
        }
    )
    return people


def display_people(people):
    """
    Отобразить список людей.
    """
    if people:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 20
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                "№",
                "Ф.И.О.",
                "Знак Зодиака",
                "Дата рождения"
            )
        )
        print(line)
        # Вывести данные о всех людях.
        for idx, human in enumerate(people, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>20} |'.format(
                    idx,
                    human['name'],
                    human['zodiac'],
                    ' '.join((str(i) for i in human['year']))
                )
            )
        print(line)


def whois(people):
    """
    Выбрать человека по фамилии.
    """
    who = input('Кого ищем?: ')
    count = 0
    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 30,
        '-' * 20,
        '-' * 20
    )
    print(line)
    print(
        '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
            "№",
            "Ф.И.О.",
            "Знак Зодиака",
            "Дата рождения"
        )
    )
    print(line)
    for i, num in enumerate(people, 1):
        if who == num['name']:
            count += 1
            print(
                '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                    count,
                    num['name'],
                    num['zodiac'],
                    ' '.join((str(i) for i in num['year']))))
    print(line)
    if count == 0:
        print('Никто не найден')


def save_people(file_name, people):
    """
    Сохранить всех работников в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(people, fout, ensure_ascii=False, indent=4)
    directory = pathlib.Path.cwd().joinpath(file_name)
    directory.replace(pathlib.Path.home().joinpath(file_name))


def load_people(file_name):
    """
    Загрузить всех людей из файла JSON
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("people")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления человека.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new human"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The human's name"
    )
    add.add_argument(
        "-z",
        "--zodiac",
        action="store",
        help="The human's zodiac"
    )
    add.add_argument(
        "-yr",
        "--year",
        action="store",
        required=True,
        help="The human's year"
    )

    # Создать субпарсер для отображения всех людей.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all people"
    )

    # Создать субпарсер для выбора людей.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the people"
    )
    select.add_argument(
        "-s",
        "--select",
        action="store",
        required=True,
        help="The required select"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить всех людей из файла, если файл существует.
    is_dirty = False
    if os.path.exists(args.filename):
        people = load_people(args.filename)
    else:
        people = []

    # Добавить человека.
    if args.command == "add":
        people = add_human(
            people,
            args.name,
            args.zodiac,
            args.year
        )
        is_dirty = True
    # Отобразить всех людей.
    elif args.command == "display":
        display_people(people)
    # Выбрать требуемых людей.
    elif args.command == "select":
        whois(people)

    # Сохранить данные в файл, если список людей был изменен.
    if is_dirty:
        save_people(args.filename, people)


if __name__ == '__main__':
    main()
