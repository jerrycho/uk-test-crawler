from json import JSONEncoder

class Question():
  def __init__(self, id, quest, type, answers):
    self.id = id
    self.quest = quest
    self.type = type
    self.answers = answers

class QuestionEncoder(JSONEncoder):
  def default(self, o):
    return o.__dict__
