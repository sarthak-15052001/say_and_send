from gpt import generate_subject


def lambda_handler(event, context):
    # Retrieve input_text from the event
    input_text = event.get("queryStringParameters", {}).get("input_text")

    if not input_text:
        return {"statusCode": 400, "body": '{"error": "Input text is missing"}'}

    try:
        # Calls the generate_subject function with input_text as an argument
        response = generate_subject(input_text=input_text)

        # Return the response
        return {
            "statusCode": 200 if "subject" in response else 500,     #  Sets the status code to 200 if the response contains a key "subject", Otherwise, sets the status code to 500, indicating an internal server error.
            "body": str(response)           # In AWS Lambda when using API Gateway, the response body must be in string format becz it expects the o/p in JSON String when interacting with HTTP endpoints.                                
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f'{{"error": "{str(e)}"}}'
        }