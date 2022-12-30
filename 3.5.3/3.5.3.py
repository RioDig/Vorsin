import sqlite3
import pandas as pd
from typing import Dict, Any


def sort_dict_area(unsorted_dict: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Метод для сортировки словаря по городам вакансии

    :param unsorted_dict: Исходный словарь
    :return: Возвращает отсортированный словарь
    """
    sorted_tuples = sorted(unsorted_dict.items(), key=lambda item: item[1], reverse=True)[:10]
    sorted_dict = {key: value for key, value in sorted_tuples}
    return sorted_dict

profession_name = input("Введите название профессии: ")
profession_name = f"%{profession_name}%"
connect = sqlite3.connect("vacancy_db.sqlite")
cursor = connect.cursor()

db_length = pd.read_sql("SELECT COUNT(*) FROM 'vacancy_db.sqlite'", connect).to_dict()["COUNT(*)"][0]


year_salary_groups = pd.read_sql(
    "SELECT SUBSTR(published_at, 1, 4) AS year, ROUND(AVG(salary)) FROM 'vacancy_db.sqlite' GROUP BY year", connect)
year_salary_dict = dict(year_salary_groups[["year", "ROUND(AVG(salary))"]].to_dict("split")["data"])


year_vacancy_groups = pd.read_sql(
    "SELECT SUBSTR(published_at, 1, 4) AS year, COUNT(name) FROM 'vacancy_db.sqlite' GROUP BY year", connect)
year_vacancy_dict = dict(year_vacancy_groups[["year", "COUNT(name)"]].to_dict("split")["data"])


profession_year_salary_groups = pd.read_sql(
    "SELECT SUBSTR(published_at, 1, 4) AS year, ROUND(AVG(salary)) FROM 'vacancy_db.sqlite' "
    "WHERE name LIKE :profession_name "
    "GROUP BY year",
    connect, params=[profession_name])
profession_year_salary_dict = dict(profession_year_salary_groups[["year", "ROUND(AVG(salary))"]].to_dict("split")["data"])


profession_year_vacancy_groups = pd.read_sql(
    "SELECT SUBSTR(published_at, 1, 4) AS year, COUNT(name) FROM 'vacancy_db.sqlite' "
    "WHERE name LIKE :profession_name "
    "GROUP BY year",
    connect, params=[profession_name])
profession_year_vacancy_dict = dict(profession_year_vacancy_groups[["year", "COUNT(name)"]].to_dict("split")["data"])


area_salary_groups = pd.read_sql(
    "SELECT area_name, ROUND(AVG(salary)), COUNT(area_name) FROM 'vacancy_db.sqlite' "
    "GROUP BY area_name "
    "ORDER BY COUNT(area_name) DESC ", connect)
area_salary_groups = area_salary_groups[area_salary_groups["COUNT(area_name)"] >= 0.01 * db_length]
area_salary_dict = dict(area_salary_groups[["area_name", "ROUND(AVG(salary))"]].to_dict("split")["data"])
area_salary_dict = sort_dict_area(area_salary_dict)


area_vacancy_groups = pd.read_sql("SELECT area_name, COUNT(area_name) FROM 'vacancy_db.sqlite' "
                                  "GROUP BY area_name "
                                  "ORDER BY COUNT(area_name) DESC "
                                  "LIMIT 10", connect)
area_vacancy_groups["COUNT(area_name)"] = round(area_vacancy_groups["COUNT(area_name)"] / db_length, 2)
area_vacancy_dict = dict(area_vacancy_groups[["area_name", 'COUNT(area_name)']].to_dict("split")["data"])

print(f"Динамика уровня зарплат по годам: {year_salary_dict}")
print(f"Динамика количества вакансий по годам: {year_vacancy_dict}")
print(f"Динамика уровня зарплат по годам для выбранной профессии: {profession_year_salary_dict}")
print(f"Динамика количества вакансий по годам для выбранной профессии: {profession_year_vacancy_dict}")
print(f"Уровень зарплат по городам (в порядке убывания): {area_salary_dict}")
print(f"Доля вакансий по городам (в порядке убывания): {area_vacancy_dict}")