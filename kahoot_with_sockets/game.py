"""
Execute a Kahoot game which is provided with questions and answers from a server
"""

import CONSTANTSs
from socket import *
from threading import Thread
import time
from tkinter import *


def find_widgets(tk_frame: LabelFrame):

    """
    Find all widgets existing in a given frame
    :param: tk_frame: A frame with widgets.
    :return: None
    """
    lst_of_widgets = tk_frame.winfo_children()
    for item in lst_of_widgets:
        if item.winfo_children():
            lst_of_widgets.extend(item.winfo_children())
    return lst_of_widgets


def true_answer():

    """
    Clear both the main and answer frames and put a "True" label on the
    answer frame
    Then send a massage to a server to provide further information
    :return: None.
    """
    txt = "True! Well done:)"
    CONSTANTSs.count_true += 1
    CONSTANTSs.count_game += 1
    lst_of_widgets = find_widgets(answer_frame)
    for widget in lst_of_widgets:
        widget.grid_forget()
    label = Label(answer_frame, text=txt)
    label.grid(row=5, column=1)
    lst_of_widgets = find_widgets(kahoot_frame)
    for widget in lst_of_widgets:
        widget.grid_forget()
    if CONSTANTSs.count_game == 3:
        txt = Label(kahoot_frame, text=f"Quiz ended, you were right in "
                                       f"{CONSTANTSs.count_true} answers")
        txt.grid()
        answer_frame.destroy()
    client.send(b'True')


def false_answer():

    """
    Clear both the main and answer frames and put a "False" label on the
    answer frame
    Then send a massage to a server to provide further information
    :return: None.
    """
    txt = "Wrong! Maybe next time!"
    CONSTANTSs.count_game += 1
    lst_of_widgets = find_widgets(answer_frame)
    for widget in lst_of_widgets:
        widget.grid_forget()
    label = Label(answer_frame, text=txt)
    label.grid(row=5, column=1)
    lst_of_widgets = find_widgets(kahoot_frame)
    for widget in lst_of_widgets:
        widget.grid_forget()
    if CONSTANTSs.count_game == 3:
        txt = Label(kahoot_frame, text=f"Quiz ended, you were right in "
                                f"{CONSTANTSs.count_true} answers")
        txt.grid()
        answer_frame.destroy()
    client.send(b'False')


def game(question: str, answer1: str, answer2: str, answer3: str, answer4: str,
         corr: int):

    """
    Define buttons for the the given question and answers
    according to the number of the correct answer and grid them into a frame
    :param question: A question.
    :param answer1: Answer 1.
    :param answer2: Answer 2.
    :param answer3: Answer 3.
    :param answer4: Answer 4.
    :param corr: The number of the correct answer.
    :return: None.
    """
    text = Label(kahoot_frame, text="welcome to Kahoot!", fg="red")
    ques = Label(kahoot_frame, text=question, fg="blue")
    if corr == 1:
        ans1 = Button(kahoot_frame, text=answer1, command=true_answer, bg="yellow",
                      padx=51.5)
        ans2 = Button(kahoot_frame, text=answer2, command=false_answer, bg="blue",
                      padx=57)
        ans3 = Button(kahoot_frame, text=answer3, command=false_answer, bg="red",
                      padx=50)
        ans4 = Button(kahoot_frame, text=answer4, command=false_answer, bg="green",
                      padx=50)
    elif corr == 2:
        ans1 = Button(kahoot_frame, text=answer1, command=false_answer, bg="yellow",
                      padx=51.5)
        ans2 = Button(kahoot_frame, text=answer2, command=true_answer, bg="blue",
                      padx=57)
        ans3 = Button(kahoot_frame, text=answer3, command=false_answer, bg="red",
                      padx=50)
        ans4 = Button(kahoot_frame, text=answer4, command=false_answer, bg="green",
                      padx=50)
    elif corr == 3:
        ans1 = Button(kahoot_frame, text=answer1, command=false_answer, bg="yellow",
                      padx=51.5)
        ans2 = Button(kahoot_frame, text=answer2, command=false_answer, bg="blue",
                      padx=57)
        ans3 = Button(kahoot_frame, text=answer3, command=true_answer, bg="red",
                      padx=50)
        ans4 = Button(kahoot_frame, text=answer4, command=false_answer, bg="green",
                      padx=50)
    else:
        ans1 = Button(kahoot_frame, text=answer1, command=false_answer, bg="yellow",
                      padx=51.5)
        ans2 = Button(kahoot_frame, text=answer2, command=false_answer, bg="blue",
                      padx=57)
        ans3 = Button(kahoot_frame, text=answer3, command=false_answer, bg="red",
                      padx=50)
        ans4 = Button(kahoot_frame, text=answer4, command=true_answer, bg="green",
                      padx=50)
    space = Label(kahoot_frame, text="")
    text.grid(row=0, column=1)
    ques.grid(row=1, column=1)
    space.grid(row=2, column=0)
    ans1.grid(row=3, column=0)
    ans2.grid(row=3, column=2)
    ans3.grid(row=4, column=0)
    ans4.grid(row=4, column=2)


def run():

    """
    A threaded function which receive a question, correct answer number
    and answers from a socket server and call the game function with them
    in an infinite loop
    :return: None.
    """

    if CONSTANTSs.count_game == 3:
        names = client.recv(2048).decode()
        str1 = Label(names_frame, text=names)
        str1.grid(row=3, column=1)
        time.sleep(5)
        client.close()

    time.sleep(0.1)
    while True:
        names = client.recv(2048).decode()
        client.send(b'Ok!')
        title = Label(names_frame, text="answer frame:", bg="red")
        title.grid(row=1, column=1)
        space = Label(names_frame, text="")
        space.grid(row=2, column=1)
        str1 = Label(names_frame, text=names)
        str1.grid(row=3, column=1)
        question = client.recv(2048).decode()
        client.send(b'hi')
        answer1 = client.recv(2048).decode()
        client.send(b'hi')
        answer2 = client.recv(2048).decode()
        client.send(b'hi')
        answer3 = client.recv(2048).decode()
        client.send(b'hi')
        answer4 = client.recv(2048).decode()
        client.send(b'hi')
        corr = int(client.recv(2048).decode())
        client.send(b'hi')
        game(question, answer1, answer2, answer3, answer4, corr)


if __name__ == '__main__':
    root = Tk()
    kahoot_frame = LabelFrame(root)
    kahoot_frame.grid(row=1, column=1)
    answer_frame = LabelFrame(root)
    answer_frame.grid(row=2, column=1)
    names_frame = LabelFrame(root)
    names_frame.grid(row=1, column=2)
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((CONSTANTSs.HOST, CONSTANTSs.PORT))
    username = input(f"{client.recv(2048).decode()} ")
    client.send(username.encode())
    Thread(target=run).start()
    root.mainloop()
