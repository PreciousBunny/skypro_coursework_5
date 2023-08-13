import os
import sys
sys.path.append(os.getcwd())
from src.job_parser_application.job_parser import JobParser


def main():
    """
    Главная функция, запускает приложение по поиску вакансий.
    """

    JobParser()


if __name__ == "__main__":
    main()
