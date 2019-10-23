import unittest
from myservice.classes.quiz import Quiz, Question, Answer, LostQuizError, NonExistingAnswerError


class TestQuiz(unittest.TestCase):

    def test1_isOpen(self):
        # given
        quiz = self.createDummyQuiz()
        # then
        quiz.isOpen()

    def test2_isOpen_fail(self):
        # given
        quiz = self.createDummyQuiz()
        # when
        self.assertRaises(LostQuizError, quiz.checkAnswer, "33")
        # then
        self.assertRaises(LostQuizError, quiz.isOpen)

    def test3_NonExistingAnswer(self):
        # given
        quiz = self.createDummyQuiz()
        # then
        self.assertRaises(NonExistingAnswerError, quiz.checkAnswer, "maronn")

    def test4_question(self):
        # given
        quiz = self.createDummyQuiz()
        quiz.isLost()
        # then
        self.assertEqual(quiz.getQuestion(),{'question': "What's the answer to all questions?", 'answers': [{'answer': '33'}, {'answer': '42'}, {'answer': '1'}]})

    def createDummyQuiz(self):
        json_data = {
            "questions": [
                {
                    "question": "What's the answer to all questions?",
                    "answers": [
                        {
                            "answer": "33",
                            "correct": 0
                        },
                        {
                            "answer": "42",
                            "correct": 1
                        },
                        {
                            "answer": "1",
                            "correct": 0
                        }
                    ]
                },
                {
                    "question": "What's the answer to all questions?",
                    "answers": [
                        {
                            "answer": "33",
                            "correct": 0
                        },
                        {
                            "answer": "42",
                            "correct": 1
                        },
                        {
                            "answer": "1",
                            "correct": 0
                        }
                    ]
                }
            ]
        }
        qs = json_data['questions']
        questions = []
        for q in qs:
            question = q['question']
            answers = []
            for a in q['answers']:
                answers.append(Answer(a['answer'], a['correct']))
            question = Question(question, answers)
            questions.append(question)

        return Quiz(1, questions)
