
import zmq
import json


def validate_text(text, min_length=0, max_length=None):
    """
    Validate text against specified rules.
    """
    # check if text is None or empty string
    if text is None or text == "":
        if min_length > 0:
            return False, "Text cannot be empty"

    # check if text is only whitespace
    if text and text.strip() == "":
        if min_length > 0:
            return False, "Text cannot be empty or only whitespace"

    # get actual text length
    text_length = len(text) if text else 0

    # check minimum length
    if min_length > 0 and text_length < min_length:
        return False, f"Text must be at least {min_length} character(s) long"

    # check maximum length
    if max_length is not None and text_length > max_length:
        return False, f"Text cannot exceed {max_length} character(s)"

    # all validation passed
    return True, None


def main():
    """
    Main service loop
    Sets up ZeroMQ socket and listens for validation requests
    """
    # create zeromq context and socket
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    # bind to port 5556
    # TODO: we need to agree as a team which of our services use which ports
    # TODO: so we don't step on each other's toes
    port = 5556
    socket.bind(f"tcp://*:{port}")

    print("=" * 50)
    print("Text Validator Microservice")
    print("=" * 50)
    print(f"Status: Running")
    print(f"Port: {port}")
    print(f"Waiting for requests...")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    print()

    request_count = 0

    try:
        while True:
            # wait for request from client
            message = socket.recv_string()
            request_count += 1

            print(f"[Request #{request_count}] Received: {message}")

            try:
                # parse JSON request
                request = json.loads(message)

                # get parameters from request
                text = request.get("text", "")
                min_length = request.get("min_length", 0)
                max_length = request.get("max_length", None)

                # validate the text
                is_valid, error_message = validate_text(text, min_length, max_length)

                # create response
                response = {
                    "valid": is_valid,
                    "error": error_message
                }

                # send JSON response
                response_json = json.dumps(response)
                socket.send_string(response_json)

                print(f"[Request #{request_count}] Sent: {response_json}")
                print()

            except json.JSONDecodeError as e:
                # handle invalid JSON
                error_response = {
                    "valid": False,
                    "error": f"Invalid JSON: {str(e)}"
                }
                socket.send_string(json.dumps(error_response))
                print(f"[Request #{request_count}] Error: Invalid JSON")
                print()

            except Exception as e:
                # handle other errors
                error_response = {
                    "valid": False,
                    "error": f"Server error: {str(e)}"
                }
                socket.send_string(json.dumps(error_response))
                print(f"[Request #{request_count}] Error: {str(e)}")
                print()

    except KeyboardInterrupt:
        print("\n" + "=" * 50)
        print("Shutting down Text Validator service...")
        print(f"Total requests processed: {request_count}")
        print("=" * 50)

    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    main()