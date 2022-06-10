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
    def __init__(self, tk, scroll_list):

        self.tk = tk
        self.scroll_list = scroll_list

        self.weight = None
        self.fruit = None
        self.new_context = "none"
        self.context = "none"

        # Input for question
        self.entry = self.tk.Entry(justify='right', bg='#a8a8a8', width=100)
        self.entry.pack(side=tk.BOTTOM)

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

            self.scroll_list.insert(self.tk.END, 'شما: ' + question)

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
                self.scroll_list.insert(self.tk.END, 'بات: ' + random_answer(answers_list))

            if finished:
                self.scroll_list.insert(self.tk.END, 'لیست شما: ' + str(self.list))

            if not got_answer:
                if self.context == 'fruit' and not fruit_found:
                    self.scroll_list.insert(self.tk.END, 'بات: این میوه رو نداریم')
                else:
                    self.scroll_list.insert(self.tk.END, 'بات: نمیدونم چی بگم')

            self.entry.delete(0, self.tk.END)
        else:
            self.scroll_list.insert(self.tk.END, 'بات متصل نیست!')

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
