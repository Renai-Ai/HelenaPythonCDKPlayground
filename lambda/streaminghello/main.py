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
    Calculates n digits of Pi using the Chudnovsky formula.
    """
    getcontext().prec = n + 1
    k = 0
    a = 1
    b = 0
    c = 640320**3 // 24
    pi = 0
    i = 0
    while True:
        a = (6 * k + 1) * (2 * k + 1) * (6 * k + 5) * a // (k**3 * c)
        b = (k + 1) ** 3 * c // (24 * (2 * k + 1))
        pi += Decimal(13591409 * a + 545140134 * b) / Decimal(640320**3 * a)
        k += 1
        if len(str(pi)) > n + 2:
            break
        if i % update == 0:
            yield str(pi)
    yield str(pi)


@app.get("/")
async def root():
    return RedirectResponse(url="/demo/")


class Story(BaseModel):
    topic: Optional[str] = None


@app.post("/api/story")
def api_story(story: Story):
    if story.topic == None or story.topic == "":
        return None

    return StreamingResponse(hello_stream(story.topic), media_type="text/html")


@app.post("/events")
def api_story(story: Story):
    if story.topic == None or story.topic == "":
        return None

    return StreamingResponse(hello_stream(story.topic), media_type="text/html")


@app.post("/2015-03-31/functions/function/invocations")
def api_story(story: Story):
    if story.topic == None or story.topic == "":
        return None

    return StreamingResponse(hello_stream(story.topic), media_type="text/html")


async def hello_stream(topic: str):

    for i in range(5):
        chunk = f"chunk {i} for {topic}\n"
        yield chunk
    yield "\n"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
