"""
A server module which provide clients with questions and answers
"""

import CONSTANTS
from socket import *


def main():

    """
    Run a socket server and accept a client. Then provide them
    with questions and answers
    :return: None.
    """
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((CONSTANTS.HOST, CONSTANTS.PORT))
    s.listen(1)
    conn, addr = s.accept()
    while CONSTANTS.count_server < 3:
        question = list(CONSTANTS.information.items())[CONSTANTS.count_server][0].encode()
        answers = CONSTANTS.information[question.decode()]
        conn.send(question)
        conn.recv(2048)
        for i in answers:
            if i == 1 or i == 2 or i == 3 or i == 4:
                conn.send(str(i).encode())
            else:
                conn.send(i.encode())
            conn.recv(2048)
        conn.recv(2048)
        CONSTANTS.count_server += 1


if __name__ == '__main__':
    main()
