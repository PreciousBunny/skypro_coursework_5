from pathlib import Path
from configparser import ConfigParser
import psycopg2

# connect to db.
# CONNECT_DB = psycopg2.connect(host='localhost', database='hh_job_parser', user='postgres', password='6464')

def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file'.format(section, filename))
    return db


params_ = config()
CONN_DB = psycopg2.connect(dbname='hh_job_parser', **params_)

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