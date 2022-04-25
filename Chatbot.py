import mysql.connector
import random

connection = mysql.connector.connect(host='localhost', database='chatbot-dataset', user='root', password='hourshid2001')


def check_similarity(existing_question, asked_question):
    return existing_question == asked_question


def random_answer(array):
    random_number = random.randint(0, len(array) - 1)
    return array[random_number]


if connection.is_connected():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dataset")
    database = cursor.fetchall()

    print(database)

    context = "none"
    fruit = ""
    cost = 0

    while True:
        question = input('شما: ')
        got_answer = False

        if context == 'fruit':
            fruit = question

        if context == 'cost':
            cost = question

        answers_list = []

        for element in database:
            if element[4] == context:
                if check_similarity(element[1], question):
                    answers_list.append(element[2])
                    context = element[3]

        if len(answers_list) > 0:
            got_answer = True
            print('بات: ', random_answer(answers_list))

        if not got_answer:
            print('بات: نمیدونم چی بگم')
