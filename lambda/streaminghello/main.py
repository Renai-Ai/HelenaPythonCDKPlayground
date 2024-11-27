import boto3
import json
import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional
import random
import asyncio

app = FastAPI()

app.mount("/demo", StaticFiles(directory="static", html=True))


@app.get("/")
async def root():
    return RedirectResponse(url="/demo/")


class Story(BaseModel):
    length: Optional[int] = None


async def generate_words(length: int):
    words_list = []
    with open("words1000.txt", "r") as file:
        words_list = file.readlines()  # Read the file line by line into a list

    for i in range(length):
        random_i = random.randint(0, len(words_list) - 1)
        result = {}
        result["percentComplete"] = f"{(i + 1) / length * 100}"
        result["word"] = words_list[random_i]
        yield json.dumps(result)
        # await asyncio.sleep(0.1)


@app.post("/api/story")
def api_story(story: Story):
    if story.length == None or story.length == "":
        return None

    return StreamingResponse(generate_words(story.length), media_type="text/html")


@app.post("/events")
def api_story(story: Story):
    if story.length == None or story.length == "":
        return None

    return StreamingResponse(generate_words(story.length), media_type="text/html")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
