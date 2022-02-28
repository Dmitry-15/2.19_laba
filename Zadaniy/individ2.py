#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Разработайте аналог утилиты tree в Linux. Используйте возможности модуля argparse для
управления отображением дерева каталогов файловой системы. Добавьте дополнительные
уникальные возможности в данный программный продукт.
"""

import argparse
import pathlib
import colorama
import collections
from colorama import Fore, Style
from datetime import datetime


def tree(directory):
    print(Fore.CYAN + f'>>> {directory}')
    for path in sorted(directory.rglob('*')):
        depth = len(path.relative_to(directory).parts)
        spacer = ' ' * depth
        print(Fore.MAGENTA + Style.BRIGHT + f'{spacer} >> {path.name}')
        for new_path in sorted(directory.joinpath(path).glob('*')):
            depth = len(new_path.relative_to(directory.joinpath(path)).parts)
            spacer = '\t' * depth
            print(Fore.YELLOW + f'{spacer} > {new_path.name}')


def main(command_line=None):
    colorama.init()
    pathway = pathlib.Path.cwd()
    file_parser = argparse.ArgumentParser(add_help=False)

    # Основной парсер командной строки
    parser = argparse.ArgumentParser("tree")
    parser.add_argument(
        "--version",
        action="version",
        help="The main parser",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Субпарсер для создания файлов
    create = subparsers.add_parser(
        "touch",
        parents=[file_parser]
    )
    create.add_argument(
        "filename",
        action="store"
    )

    # Субпарсер для удаления файлов
    create = subparsers.add_parser(
        "unlink",
        parents=[file_parser]
    )
    create.add_argument(
        "filename",
        action="store"
    )

    # Субпарсер для нахождения последнего измененного файла
    create = subparsers.add_parser(
        "changed",
        parents=[file_parser]
    )
    create.add_argument(
        "filename",
        action="store"
    )

    # Субпарсер для подсчета файлов
    create = subparsers.add_parser(
        "count",
        parents=[file_parser]
    )
    create.add_argument(
        "filename",
        action="store"
    )
    args = parser.parse_args(command_line)
    if args.command == 'touch':
        directory_path = pathway / args.filename
        directory_path.touch()
        tree(pathway)
    elif args.command == "unlink":
        directory_path = pathway / args.filename
        directory_path.unlink()
        tree(pathway)
    elif args.command == "changed":
        time, file_path = max((f.stat().st_mtime, f) for f in pathlib.Path.cwd().iterdir())
        print(datetime.fromtimestamp(time), file_path)
    elif args.command == "count":
        print(collections.Counter(p.suffix for p in pathlib.Path.cwd().iterdir()))
    else:
        tree(pathway)


if __name__ == "__main__":
    main()