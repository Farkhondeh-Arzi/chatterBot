import mysql.connector
import random

from doc_term_matrix import DocTermMatrix


# Input array is possible answers
def random_answer(array):
    random_number = random.randint(0, len(array) - 1)
    return array[random_number]


class ChatterBot:
    # Connection to database
    connection = mysql.connector.connect(host='localhost',
                                         database='chatbot-dataset',
                                         user='root',
                                         password='hourshid2001')
    # Bought fruits
    list = []

    # tk is for graphic
    def __init__(self, tk):

        self.tk = tk

        self.weight = None
        self.fruit = None
        self.new_context = "none"
        self.context = "none"

        # Input for question
        self.entry = self.tk.Entry()
        self.entry.pack()

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

            question = self.entry.get()

            label = self.tk.Label(text='شما: ' + question)
            label.pack()

            got_answer = False
            finished = False
            fruit_found = False

            if self.fruit is not None and self.weight is not None:
                self.list.append([self.fruit, self.weight])
                self.fruit = None
                self.weight = None

            # Finish
            if self.doc_matrix.check_similarity_with_another_text(question, 'خداحافظ'):
                self.context = 'bye'
                finished = True

            if self.context == 'fruit':
                if self.find_fruit_from_sentence(question) is not None:
                    fruit_found = True
                    self.fruit = self.find_fruit_from_sentence(question)

            if self.context == 'cost':
                self.weight = question

            answers_list = []

            indices = self.doc_matrix.check_similarity(question)
            for index in indices:
                # database[index][3] is context
                if self.database[index][3] == self.context:
                    # database[index][2] is answer
                    answers_list.append(self.database[index][2])
                    # database[index][4] is next context
                    self.new_context = self.database[index][4]

            if len(answers_list) > 0:
                got_answer = True
                self.context = self.new_context
                label = self.tk.Label(text='بات: ' + random_answer(answers_list))
                label.pack()

            if finished:
                label = self.tk.Label(text='لیست شما: ' + str(self.list))
                label.pack()

            if not got_answer:
                if self.context == 'fruit' and not fruit_found:
                    label = self.tk.Label(text='بات: این میوه رو نداریم')
                    label.pack()
                else:
                    label = self.tk.Label(text='بات: نمیدونم چی بگم')
                    label.pack()

            self.entry.delete(0, self.tk.END)
        else:
            label = self.tk.Label(text='بات متصل نیست!')
            label.pack()

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
