
import zmq
import json


def _validate_empty_text(text, min_length):
    """Check if text is empty or whitespace when min_length requires it."""
    if min_length > 0:
        if text is None or text == "":
            return False, "Text cannot be empty"
        if text.strip() == "":
            return False, "Text cannot be empty or only whitespace"
    return True, None


def _validate_min_length(text, min_length):
    """Check if text meets minimum length requirement."""
    if min_length > 0 and len(text) < min_length:
        return False, f"Text must be at least {min_length} character(s) long"
    return True, None


def _validate_max_length(text, max_length):
    """Check if text exceeds maximum length."""
    if max_length is not None and len(text) > max_length:
        return False, f"Text cannot exceed {max_length} character(s)"
    return True, None


def validate_text(text, min_length=0, max_length=None):
    """
    Validate text against specified rules.
    """
    is_valid, error = _validate_empty_text(text, min_length)
    if not is_valid:
        return False, error

    if text is None:
        text = ""

    is_valid, error = _validate_min_length(text, min_length)
    if not is_valid:
        return False, error

    is_valid, error = _validate_max_length(text, max_length)
    if not is_valid:
        return False, error

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
                request = json.loads(message)

                # get parameters from request
                text = request.get("text", "")
                min_length = request.get("min_length", 0)
                max_length = request.get("max_length", None)

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
