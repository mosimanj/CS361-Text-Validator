# CS361-Text-Validator
## How to Request Data
### Request Parameters
* **Text**: String of input text
* **min_length** (optional): Minimum length of valid input text
* **max_length** (optional): Maximum length of valid input text

### Request Format
```
{
    "text": "example text",
    "min_length": 1,
    "max_length": 100
}
```

### Example Call
```
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")
request = {"text": "Do homework", "min_length": 1, "max_length": 100}
request_json = json.dumps(request)
socket.send_string(request_json)
```
## How to Receive Data
### Response Object
* **valid** (boolean): True if all validation passed, False otherwise
* **error** (string or null): Description of validation error if invalid, null if valid

### Response Format
#### Valid
```
{
    "valid": true,
    "error": null
}
```

#### Invalid
```
{
    "valid": false,
    "error": "Text cannot be empty"
}
```

### Example Call
```
import zmq
import json

response_json = socket.recv_string()
response = json.loads(response_json)
if response["valid"]:
    print("Text is valid!")
else:
    print(f"Validation error: {response['error']}")
socket.close()
context.term()
```
## UML Diagram
<img width="800" height="321" alt="image" src="https://github.com/user-attachments/assets/d2e185ea-cbac-49dd-9b4f-256800099287" />

[View diagram here](https://lucid.app/lucidchart/8e2141c2-6130-446f-a50f-71bae0807448/edit?viewport_loc=-193%2C10%2C1461%2C707%2C0_0&invitationId=inv_6e4d4009-3c7a-4cc6-ae24-cb33d79b596c)

## How to Run

### Start the Microservice
```bash
python text_validator.py
```

### Run the Test Program
In a separate terminal:
```bash
python test_program.py
```

### Expected Output
The microservice will display:
- Status: Running
- Port: 5556
- Request count and details

The test program will display:
- Request sent
- Response received
- Validation result
```
