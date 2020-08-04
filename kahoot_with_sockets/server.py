"""
A server module which provide clients with questions and answers
"""

import CONSTANTSs
import csv
import random
from socket import *
from threading import Thread


names_dict = {}


def main():

    """
    Run a socket server and accept a client. Then provide them
    with questions and answers
    :return: None.
    """

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((CONSTANTSs.HOST, CONSTANTSs.PORT))
    s.listen(4)
    while True:
        conn, addr = s.accept()
        conn.send(b"Welcome to Kahoot, what's your name?")
        username = conn.recv(2048).decode()
        names_dict[username] = 0
        Thread(target=run, args=(conn, username)).start()


def find_names():
    lst_of_names = list(names_dict.keys())
    names = ""
    for name in lst_of_names:
        if name != lst_of_names[-1]:
            names += name
            names += f": {names_dict[name]}, "
        else:
            names += name
            names += f": {names_dict[name]}"
    return names


def run(conn, username):
    with open('info.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
        lst = []
        for round in range(1, len(data) + 1):
            num_of_ques = random.randint(0, len(data) - 1)
            while num_of_ques in lst:
                num_of_ques = random.randint(0, len(data) - 1)
            lst.append(num_of_ques)
            info = data[num_of_ques]
            question = info[0].encode()
            answer1 = info[1].encode()
            answer2 = info[2].encode()
            answer3 = info[3].encode()
            answer4 = info[4].encode()
            corr = info[5].encode()
            names = find_names()
            conn.send(names.encode())
            conn.recv(2048)
            conn.send(question)
            conn.recv(2048)
            conn.send(answer1)
            conn.recv(2048)
            conn.send(answer2)
            conn.recv(2048)
            conn.send(answer3)
            conn.recv(2048)
            conn.send(answer4)
            conn.recv(2048)
            conn.send(corr)
            conn.recv(2048)
            answer = conn.recv(2048)
            if answer == b'True':
                names_dict[username] += 1
        names = find_names()
        conn.send(names.encode())
        del names_dict[username]


if __name__ == '__main__':
    main()
