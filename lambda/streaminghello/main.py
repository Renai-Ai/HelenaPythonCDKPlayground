import boto3
import json
import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional
import asyncio

app = FastAPI()

app.mount("/demo", StaticFiles(directory="static", html=True))

from decimal import Decimal, getcontext


async def pi_chudnovsky(n, update):
    """
    Calculates pi using the Chudnovsky formula.
    """

    getcontext().prec = n + 1  # Set the precision for decimal calculations

    C = Decimal(426880 * Decimal(10005).sqrt())
    L = Decimal(13591409)
    X = Decimal(1)
    M = Decimal(1)
    K = Decimal(6)
    S = L
    result = {}
    for i in range(1, n):
        M = (K**3 - 16 * K) * M / (i**3)
        L += Decimal(545140134)
        K += Decimal(12)
        X *= -Decimal(262537412640768000)
        S += Decimal(M * L) / X
        if i % update == 0:
            result["pi"] = str(C / S)
            result["percentComplete"] = str(i / n * 100)
            yield json.dumps(result)

    result["pi"] = str(C / S)
    result["percentComplete"] = str(i / n * 100)
    yield json.dumps(result)


@app.get("/")
async def root():
    return RedirectResponse(url="/demo/")


class Story(BaseModel):
    length: Optional[int] = None


@app.post("/api/story")
def api_story(story: Story):
    if story.length == None or story.length == "":
        return None

    return StreamingResponse(pi_chudnovsky(story.length, 1), media_type="text/html")


@app.post("/2015-03-31/functions/function/invocations")
def api_story(story: Story):
    if story.topic == None or story.topic == "":
        return None

    return StreamingResponse(pi_chudnovsky(1000, 10), media_type="text/html")


async def hello_stream(topic: str):

    for i in range(5):
        chunk = f"chunk {i} for {topic}\n"
        yield chunk
    yield "\n"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
