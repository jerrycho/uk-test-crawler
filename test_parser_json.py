from pathlib import Path
import json


json_txt = Path('test.json').read_text()
content = json.loads(json_txt)

# type and answer
for key in content['json']:
    type = content['json'][key]['type'] # single || multiple
    correct = content['json'][key]['correct']
    print(type)
    print(correct)