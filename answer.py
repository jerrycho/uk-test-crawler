from json import JSONEncoder

class Answer():
  def __init__(self, answer, correct):
    self.answer = answer
    self.correct = correct


class AnswerEncoder(JSONEncoder):
  def default(self, o):
    return o.__dict__
