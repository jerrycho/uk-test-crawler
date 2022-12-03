import codecs

import requests
import json
from bs4 import BeautifulSoup
from question import Question, QuestionEncoder
from answer import Answer
import urllib.parse
import html
from json import dumps



def get_info_by_quizid(qid):

    ploads = {'action': 'wp_pro_quiz_admin_ajax', 'func': 'quizLoadData', 'data[quizId]': qid}
    r = requests.post('https://lifeintheuktests.co.uk/wp-admin/admin-ajax.php', data= ploads)
    #print(r.text)
    content = json.loads(r.text)

    # list is declared
    id_list = []
    quest_list = []
    type_list = []
    answers_list = []
    correct_list = []


    #############################
    # type and answer
    #############################
    # type and answer
    for key in content['json']:
        type = content['json'][key]['type'] # single || multiple
        correct = content['json'][key]['correct']
        type_list.append(type)
        correct_list.append(correct)

    #############################
    # question part
    #############################
    html_text = content['content']
    soup = BeautifulSoup(html_text, 'html.parser')

    # found all <li class="theorypass_listItem">
    for li in soup.find_all("li", {"class": "theorypass_listItem"}):
        # Question
        # <div><p>Which Two British film actors have recently won Oscars?</p></div>
        question_dev = li.find("div", {"class": "theorypass_question_text"})
        question_str = question_dev.find("p").text
        question_str = urllib.parse.unquote(question_str)

        #question_str = urllib.parse.unquote(question_dev.find("p").text).encode('unicode-escape').replace(b'\\\\', b'\\').decode('unicode-escape')
        question_str = html.escape(question_str)
        question_str = question_str.replace("\u2019", "'")
        question_str = question_str.replace("\u2018", "'")
        question_str = question_str.replace("\u201c", "'")
        question_str = question_str.replace("\u201c", "'")

        question_str = question_str.replace("\u00a0", " ")

        quest_list.append(question_str)

        id = li.find("ul", {"class": "theorypass_questionList"}).get("data-question_id")
        id_list.append(id)

        # answer
        # <div class="question_text_area">
        answers = []
        for answer in li.find_all("div", {"class": "question_text_area"}):
            #print(answer.text.strip())
            answers.append(answer.text.strip())
        answers_list.append(answers)

    question_list = []

    for i in range(len(quest_list)):
      my_answer_list = []
      # loop answers_list[i]
      for x in range(len(answers_list[i])):
        my_answer_list.append(
            Answer(
                answer=answers_list[i][x],
                correct=correct_list[i][x]==1
            )
        )

      question_list.append(
          Question(
              id=id_list[i],
              quest=quest_list[i],
              type=type_list[i],
              answers=my_answer_list
          )
      )

    print(QuestionEncoder().encode(question_list))

    with codecs.open('test'+str(qid)+'.json', 'w', 'utf8') as f:
       f.write(QuestionEncoder().encode(question_list))

for i in range(1, 46):
    get_info_by_quizid(i)
