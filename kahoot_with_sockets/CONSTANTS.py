"""
Constants module
"""

import csv


HOST = '192.168.14.39'
PORT = 8001
count_server = 0
count_game = 0
count_true = 0
information = [["what is my name?", "elad", "matan", "losha", "moshe", 1],
               ["what is my teacher's name?", "elad", "matan", "losha", "moshe",
                                              3],
               ["what is my brother's name?", "elad", "matan", "losha", "moshe",
                                              2]]
with open('info.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(information)
