import os
import sys
sys.path.append(os.getcwd())
from config import QUERIES_PATH


def read_queries_sql():
    """
    Функция читает и сохраняет в словаре SQL-запросы из файла.
    """
    queries_sql = {}
    current_query_name = None
    current_query = ""

    with open(QUERIES_PATH, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("--"):
                if current_query_name and current_query:
                    queries_sql[current_query_name] = current_query.strip()
                current_query_name = line.lstrip("--").strip()
                current_query = ""
            else:
                current_query += line
    if current_query_name and current_query:
        queries_sql[current_query_name] = current_query.strip()
        
    return queries_sql
