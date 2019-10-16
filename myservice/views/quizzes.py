from flakon import JsonBlueprint
from flask import request, jsonify, abort
from myservice.classes.quiz import Quiz, Question, Answer
from myservice.classes.quiz import NonExistingAnswerError, LostQuizError
from myservice.classes.quiz import CompletedQuizError

quizzes = JsonBlueprint('quizzes', __name__)

_LOADED_QUIZZES = {}  # list of available quizzes
_QUIZNUMBER = 0  # index of the last created quizzes


@quizzes.route("/quizzes", methods=['POST', 'GET'])
def all_quizzes():
    global _LOADED_QUIZZES
    global _QUIZNUMBER

    try:

        if 'POST' == request.method:
            result = create_quiz(request)
        elif 'GET' == request.method:
            result = get_all_quizzes(request)

    except BaseException:
        abort(400)  # Bad Request

    return result


@quizzes.route("/quizzes/loaded", methods=['GET'])
# returns the number of quizzes currently loaded in the system
def loaded_quizzes():
    return jsonify({'loaded_quizzes': len(_LOADED_QUIZZES)})


@quizzes.route("/quiz/<int:id>", methods=['GET', 'DELETE'])
def single_quiz(id):
    global _LOADED_QUIZZES
    result = ""
    id = str(id)

    exists_quiz(id)

    if 'GET' == request.method:
        result = jsonify(Quiz.serialize(_LOADED_QUIZZES[id]))

    elif 'DELETE' == request.method:
        # delete a quiz and get back number of answered questions
        quiz = _LOADED_QUIZZES[id]
        del _LOADED_QUIZZES[id]
        result = jsonify({"answered_questions": quiz.currentQuestion,
                          "total_questions": len(quiz.questions)})

    return result


@quizzes.route("/quiz/<int:id>/question", methods=['GET'])
def play_quiz(id):
    global _LOADED_QUIZZES
    result = ""
    id = str(id)

    exists_quiz(id)

    if 'GET' == request.method:
        try:
            result = jsonify(Quiz.getQuestion(_LOADED_QUIZZES[id]))
        except CompletedQuizError:
            result = jsonify({"msg": "completed quiz"})
        except LostQuizError:
            result = jsonify({"msg": "you lost!"})

    return result


@quizzes.route("/quiz/<int:id>/question/<string:answer>", methods=['PUT'])
def answer_question(id, answer):
    global _LOADED_QUIZZES
    result = ""
    id = str(id)
    exists_quiz(id)
    quiz = _LOADED_QUIZZES[id]

    try:
        Quiz.isOpen(quiz)
        if 'PUT' == request.method:
            try:
                result = Quiz.checkAnswer(quiz, answer)
            except CompletedQuizError:
                result = "you won 1 million clams!"
            except NonExistingAnswerError:
                result = "non-existing answer!"
    except CompletedQuizError:
        result = "completed quiz"
    except LostQuizError:
        result = "you lost!"

    return jsonify({"msg": result})


############################################
# USEFUL FUNCTIONS BELOW (use them, don't change them)
############################################


def create_quiz(request):
    global _LOADED_QUIZZES, _QUIZNUMBER

    json_data = request.get_json()
    qs = json_data['questions']
    questions = []
    for q in qs:
        question = q['question']
        answers = []
        for a in q['answers']:
            answers.append(Answer(a['answer'], a['correct']))
        question = Question(question, answers)
        questions.append(question)

    _LOADED_QUIZZES[str(_QUIZNUMBER)] = Quiz(_QUIZNUMBER, questions)
    _QUIZNUMBER += 1

    return jsonify({'quiznumber': _QUIZNUMBER - 1})


def get_all_quizzes(request):
    global _LOADED_QUIZZES

    return jsonify(loadedquizzes=[e.serialize() for e in _LOADED_QUIZZES.values()])


def exists_quiz(id):
    if int(id) > _QUIZNUMBER:
        abort(404)  # error 404: Not Found, i.e. wrong URL, resource does not exist
    elif not (id in _LOADED_QUIZZES):
        abort(410)  # error 410: Gone, i.e. it existed but it's not there anymore
