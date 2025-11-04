# CS361-Text-Validator
## How to Request Data
### Request Parameters
* **Text**:String of input text
* **Min_length** (optional): Maximum length of valid input text
* **Min_length** (optional): Minimum length of valid input text

### Example Call
```
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")
request = {
"text": "Do homework",
"min_length": 1,
"max_length": 100
}
request_json = json.dumps(request)
socket.send_string(request_json)
response_json = socket.recv_string()
response = json.loads(response_json)
if response["is_valid"]:
print("Text is valid!")
else:
print(f"Validation error: {response['message']}")
socket.close()
context.term()
```
## How to Receive Data
### Response Object
* **valid** (boolean): True if all validation passed, False otherwise
* **error** (string or null): Description of validation error if invalid, null if valid
### Example Call
```
# Create context and socket
context = zmq.Context()
socket = context.socket(zmq.REP)
# Bind to port 5556
socket.bind("tcp://*:5556")
while True:
# Receive request
message = socket.recv_string()
request = json.loads(message)
# Extract parameters
text = request.get("text", "")
min_length = request.get("min_length", 0)
max_length = request.get("max_length", None)
# Validate text
is_valid, error_message = validate_text(text, min_length, max_length)
# Create response
response = {
"valid": is_valid,
"error": error_message
}
# Send response
response_json = json.dumps(response)
socket.send_string(response_json)
CLIENT/OTHER PROGRAMS
# Receive response response_
json = socket.recv_string()
response = json.loads(response_json)
# Use validation result
if response["valid"]:
# Proceed with valid text
process_text(text)
else:
# Display error to
user display_error(response["error"])
```
## UML Diagram
