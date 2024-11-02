import json

def handler(event, context):
    try:
        # body = {
        #     "message": f"Echo from Python Lambda {event["body"]["message"]}",
        # }

        eventStr = str(event.get("body"))
        messageJSON = json.loads(eventStr)
        message = messageJSON.get("message")
        # content = json.loads(eventStr)


        body = {
            "message": str(message) + " Echo from Python Lambda 2024-Oct-28",
        }
    except Exception as e:
        body = {
            "message": f"Error: {str(e)}"
        }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
    }

    return response