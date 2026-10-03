#!/usr/bin/env python
import os
import sys


def main() -> None:
    """Запустить административные команды Django."""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "homeparty.settings",
    )

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
