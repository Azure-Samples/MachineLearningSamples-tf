import base64
import json
from webservice_driver import init, run

im_name = '/tmp/test/0.png'

# prepare input  
with open(im_name, 'rb') as file:
  encoded = base64.b64encode(file.read())
payload = []
payload.append("{}".format(encoded))
reqStr = json.dumps(payload)

# score the image
init()
pred_letter = run(reqStr)
print(pred_letter)
