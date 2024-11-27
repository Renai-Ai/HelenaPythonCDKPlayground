import json
from aws_lambda_powertools.utilities.streaming import streamify_response, ResponseStream
import time


@streamify_response
def handler(event, context):
    response_stream = ResponseStream()

    for i in range(5):
        data = {"message": f"Chunk 2024 {i}"}
        response_stream.write(json.dumps(data))
        time.sleep(1)

    return response_stream.close()
