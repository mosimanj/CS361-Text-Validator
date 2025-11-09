import zmq
import json


def test_validator(description, text, min_length=0, max_length=None):
    """Run a single test case"""
    print(f"\n{'=' * 50}")
    print(f"TEST: {description}")
    print(f"{'=' * 50}")

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")

    request = {"text": text, "min_length": min_length}
    if max_length:
        request["max_length"] = max_length

    print(f"Request: {json.dumps(request, indent=2)}")

    socket.send_string(json.dumps(request))
    response = json.loads(socket.recv_string())

    print(f"Response: {json.dumps(response, indent=2)}")

    if response["valid"]:
        print("✓ Text is valid!")
    else:
        print(f"✗ Validation error: {response['error']}")

    socket.close()
    context.term()


if __name__ == "__main__":
    print("TEXT VALIDATOR TEST PROGRAM")
    print("Testing various validation scenarios...\n")

    # valid text
    test_validator("Valid text with valid length", "Do homework", 1, 100)

    # empty text
    test_validator("Empty text (should fail)", "", 1, 100)

    # text too short
    test_validator("Text below minimum length", "Hi", 5, 100)

    # text too long
    test_validator("Text exceeds maximum length", "a" * 101, 1, 100)

    # whitespace only
    test_validator("Whitespace only (should fail)", "   ", 1, 100)

    # valid text at boundaries
    test_validator("Text exactly at max length", "a" * 100, 1, 100)

    print(f"\n{'=' * 50}")
    print("ALL TESTS COMPLETE")
    print(f"{'=' * 50}")