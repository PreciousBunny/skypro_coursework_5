from pathlib import Path
import psycopg2

# connect to db.
CONNECT_DB = psycopg2.connect(host='localhost', database='hh_job_parser', user='postgres', password='6464')

QUERIES_PATH = str(Path(__file__).resolve().parent / "src" / "database" / "queries.sql")

EMPLOYERS_VACANCY_ID = {
    "VK": 15478,
    "Яндекс": 1740,
    "АльфаБанк": 80,
    "Сбербанк": 3529,
    "Тинькофф": 78638,
    "МТС": 3776,
    "Эталон": 140987,
    "SetlGroup": 2864629,
    "ПИК": 12550,
    "ЛУКОЙЛ": 907345,
    "АЛРОСА": 92288,
    "НЛМК": 988387,
    "MOEX": 4307,
    "ЦРТ": 4585,
    "ЛИГРЕС": 4919467,
    "ЛЕНТА": 7172
}