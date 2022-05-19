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

            cursor.execute("SELECT * FROM available_fruits")
            self.available_fruits = [item[0] for item in cursor.fetchall()]

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
                fruit_found = False

                if fruit is not None and cost is not None:
                    self.list.append([fruit, cost])
                    fruit = None
                    cost = None

                if self.doc_matrix.check_similarity_with_another_text(question, 'خداحافظ'):
                    context = 'bye'
                    finished = True

                if context == 'fruit':
                    if self.find_fruit_from_sentence(question) is not None:
                        fruit_found = True
                        fruit = self.find_fruit_from_sentence(question)

                if context == 'cost':
                    cost = question

                answers_list = []

                indices = self.doc_matrix.check_similarity(question)
                for index in indices:
                    # database[index][4] is context
                    if self.database[index][3] == context:
                        # database[index][2] is answer
                        answers_list.append(self.database[index][2])
                        # database[index][3] is next context
                        new_context = self.database[index][4]

                if len(answers_list) > 0:
                    got_answer = True
                    context = new_context
                    print('بات:', random_answer(answers_list))

                if finished:
                    print('لیست شما:', self.list)
                    break

                if not got_answer:
                    if context == 'fruit' and not fruit_found:
                        print('این میوه رو نداریم.')
                    else:
                        print('بات: نمیدونم چی بگم')

        else:
            print("بات متصل نیست!")

    def available_questions(self):

        questions = []

        for element in self.database:
            questions.append(element[1])

        return questions

    def find_fruit_from_sentence(self, sentence):
        split_sentence = sentence.split()

        for word in split_sentence:
            if self.available_fruits.__contains__(word):
                return word
