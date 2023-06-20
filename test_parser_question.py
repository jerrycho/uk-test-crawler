import urllib
from pathlib import Path
from bs4 import BeautifulSoup

html_text = Path('test.html').read_text()
soup = BeautifulSoup(html_text, 'html.parser')

# found all <li class="theorypass_listItem">
for li in soup.find_all("li", {"class": "theorypass_listItem"}):
    # Question
    # <div><p>Which Two British film actors have recently won Oscars?</p></div>
    question_dev = li.find("div", {"class": "theorypass_question_text"})
    my_question_str = li.find("ul", {"class": "theorypass_questionList"}).get("data-question_id") + ': ' +urllib.parse.unquote(question_dev.find("p").text)
    print("my_question= "+ my_question_str)



    # id <ul class="theorypass_questionList" data-question_id="8"
    question_id = li.find("ul", {"class": "theorypass_questionList"})
    # print(question_id)


    # answer
    # <div class="question_text_area">
    #for answer in li.find_all("div", {"class": "question_text_area"}):
        #print(answer.text.strip())

    print('-------')
