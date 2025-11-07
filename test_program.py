import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")
request = {"text": "Do homework", "min_length": 1, "max_length": 100}
request_json = json.dumps(request)
socket.send_string(request_json)
response_json = socket.recv_string()
response = json.loads(response_json)
if response["valid"]:
    print("Text is valid!")
else:
    print(f"Validation error: {response['error']}")
socket.close()
context.term()
