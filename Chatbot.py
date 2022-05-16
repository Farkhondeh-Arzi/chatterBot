import mysql.connector
import random

from doc_term_matrix import DocTermMatrix


def random_answer(array):
    random_number = random.randint(0, len(array) - 1)
    return array[random_number]


class ChatterBot:
    connection = mysql.connector.connect(host='localhost',
                                         database='chatbot-dataset',
                                         user='root',
                                         password='hourshid2001')
    list = []

    def __init__(self):
        if self.connection.is_connected():
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM dataset")
            self.database = cursor.fetchall()
            self.connected = True

            questions = self.available_questions()
            self.doc_matrix = DocTermMatrix(questions)
        else:
            self.connected = False

    def start_chat(self):

        if self.connected:

            context = "none"
            new_context = "none"
            fruit = None
            cost = None

            while True:

                question = input('شما: ')
                got_answer = False
                finished = False

                if fruit is not None and cost is not None:
                    self.list.append([fruit, cost])
                    fruit = None
                    cost = None

                if self.doc_matrix.check_similarity_with_another_text(question, 'خداحافظ'):
                    context = 'bye'
                    finished = True

                if context == 'fruit':
                    fruit = question

                if context == 'cost':
                    cost = question

                answers_list = []

                indices = self.doc_matrix.check_similarity(question)
                for index in indices:
                    # database[index][4] is context
                    if self.database[index][4] == context:
                        # database[index][2] is answer
                        answers_list.append(self.database[index][2])
                        # database[index][3] is next context
                        new_context = self.database[index][3]

                if len(answers_list) > 0:
                    got_answer = True
                    context = new_context
                    print('بات: ', random_answer(answers_list))

                if finished:
                    print('لیست شما: ', self.list)
                    break

                if not got_answer:
                    print('بات: نمیدونم چی بگم')

    def available_questions(self):

        questions = []

        for element in self.database:
            questions.append(element[1])

        return questions
