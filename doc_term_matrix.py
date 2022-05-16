import numpy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DocTermMatrix:
    count_vectorizer = TfidfVectorizer()

    def __init__(self, documents):
        self.documents = documents
        self.sparse_matrix = self.count_vectorizer.fit_transform(self.documents)

    def check_similarity(self, text):

        proper_answers = []

        text_sparse_matrix = self.count_vectorizer.transform([text])

        similarities = cosine_similarity(self.sparse_matrix, text_sparse_matrix)

        maximum = numpy.amax(similarities)

        if maximum > 0:
            proper_answers = numpy.where(similarities == maximum)[0]

        return proper_answers

    def check_similarity_with_another_text(self, text1, text2):

        text1_sparse_matrix = self.count_vectorizer.transform([text1])
        text2_sparse_matrix = self.count_vectorizer.transform([text2])
        similarity = cosine_similarity(text1_sparse_matrix, text2_sparse_matrix)

        if similarity > 0.5:
            return True
        else:
            return False
