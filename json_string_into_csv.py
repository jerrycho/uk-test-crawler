import json
import csv

#with codecs.open('test'+str(qid)+'.json', 'w', 'utf8') as f:

json_file = 'test1.json'
csv_file = 'output.csv'

import json
import csv

json_file = 'test1.json'
csv_file = 'output.csv'

# 建立一個 set 來儲存已經寫入 CSV 檔案的值
written_set = set()

# 開啟 JSON 檔案data
for i in range(1, 46):
    with open('test' + str(i) + '.json', 'r') as f:
        datas = json.load(f)
        for element in datas:
            quest = element['quest']
            # check question was at set or not
            if quest not in written_set:
                written_set.add(quest)
            for answers in element['answers']:
                answer = answers['answer']
                if answer not in written_set:
                    written_set.add(answer)

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    for str in written_set:
        print("set:" + str)
        writer.writerow([str])



