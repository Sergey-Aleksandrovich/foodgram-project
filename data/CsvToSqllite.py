import csv
import sqlite3

# def csv_reader(file_obj):
#     """
#     Read a csv file
#     """
#     result = [['title', 'dimension', 'id']]
#     count = 0
#     reader = csv.reader(file_obj)
#     for row in reader:
#         count += 1
#         row.append(count)
#         result.append(row)
#     return result
#
#
# def list_to_csv(list_obj):
#     """
#     Write a csv file
#     """
#     with open('new_ingredients.csv', 'w', encoding='utf8',
#               newline='') as f:
#         writer = csv.writer(f)
#         writer.writerows(list_obj)


def add_data_in_sqllite(csv_file, table_name):
    """
    Add csv in sqllite
    """
    con = sqlite3.connect("../db.sqlite3")
    with con:
        cur = con.cursor()
        with open(f'{csv_file}', encoding='utf-8') as file:
            data = csv.reader(file)
            columns = f"{tuple(data.__next__())}"
            for row in data:
                sql = f"INSERT INTO {table_name}{columns} VALUES{tuple(row)}"
                cur.execute(sql)


if __name__ == "__main__":
    csv_path_ingredients = "ingredients.csv"
    with open(csv_path_ingredients, "r", encoding='utf8', ) as file1_obj:
        add_data_in_sqllite(csv_path_ingredients, 'recipes_ingredientlist')

