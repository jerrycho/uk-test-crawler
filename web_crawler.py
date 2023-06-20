import codecs
import csv

import requests
import json
from bs4 import BeautifulSoup
from question import Question, QuestionEncoder
from answer import Answer
import urllib.parse
import html
from json import dumps



def get_info_by_quizid(qid, hashmap):

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
        answer_zh = answers_list[i][x]
        try:
            answer_zh=hashmap[answers_list[i][x]]
        except:
            print("")
        my_answer_list.append(
            Answer(
                answer = answers_list[i][x],
                answer_zh=answer_zh,
                correct=correct_list[i][x]==1
            )
        )

      quest_zh = quest_list[i]
      try:
          quest_zh = hashmap[quest_list[i]]
      except:
          print("")
      question_list.append(

          Question(
              id=id_list[i],
              quest=quest_list[i],
              quest_zh= quest_zh,
              type=type_list[i],
              answers=my_answer_list
          )
      )

    #print(QuestionEncoder().encode(question_list))

    with codecs.open('test'+str(qid)+'.json', 'w', 'utf8') as f:
        json_str = json.dumps(question_list,  ensure_ascii=False, default=question_encoder)
        print(json_str)
        f.write(json_str)
       #f.write(QuestionEncoder().encode(question_list), ensure_ascii=False)


def question_encoder(obj):
  if isinstance(obj, Question):
    return {'id': obj.id, 'quest': obj.quest, 'quest_zh': obj.quest_zh, 'type': obj.type, 'answers': obj.answers}
  elif isinstance(obj, Answer):
    return {'answer': obj.answer, 'answer_zh': obj.answer_zh, 'correct': obj.correct}

####
# 建立一個空的 hashmap，用來儲存每一列的 dictionary
csv_data = {}

# 開啟 CSV 檔案
with open('word-chinese.csv',  encoding="utf8", newline='') as csvfile:
    # 建立 CSV 讀取器
    reader = csv.reader(csvfile)
    print(reader)
    # 使用 next() 方法讀取第一列的資料，通常是欄位名稱，這邊我們先忽略不處理
    next(reader)

    # 逐一讀取每一列
    for row in reader:

        # 將 dictionary 儲存到 hashmap 中，使用第一個欄位的值當作 key
        csv_data[row[0]] = row[1]

# 印出 hashmap 中的所有資料
for key, value in csv_data.items():
    print(key, value)

for i in range(1, 46):
    get_info_by_quizid(i, csv_data)
