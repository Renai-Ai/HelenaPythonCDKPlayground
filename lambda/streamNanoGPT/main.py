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
import subprocess

app = FastAPI()

app.mount("/demo", StaticFiles(directory="static", html=True))


@app.get("/")
async def root():
    return RedirectResponse(url="/demo/")


class Story(BaseModel):
    length: Optional[int] = None


async def generate_words2(length: int):
    r = {}
    r["percentComplete"] = f"0%"
    r["word"] = "Generating story...\n"
    yield json.dumps(r)
    result = subprocess.run(
        ["python", "sample.py --out_dir=out-shakespeare-char --device=cpu"],
        # ["ls", "-la"],
        capture_output=True,  # Python >= 3.7 only
        text=True,  # Python >= 3.7 only
    )
    r = {}
    r["percentComplete"] = f"100%"
    r["word"] = result.stdout
    yield json.dumps(r)


async def generate_words(length: int):
    r = {}
    r["percentComplete"] = f"0%"
    r["word"] = "Generating story...\n"
    yield json.dumps(r)
    cmd = [
        "python",
        "sample.py",
        "--out_dir=out-shakespeare-char",
        "--device=cpu",
        "--num_samples=1",
        "--max_new_tokens=500",
    ]
    # cmd = ["ls", "-la"]
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True, bufsize=1
    )
    NLINES = 100
    line = 1
    for stdout_line in iter(popen.stdout.readline, ""):
        r["percentComplete"] = f"{line/NLINES * 100}%"
        r["word"] = stdout_line
        line += 1
        yield json.dumps(r)
    popen.stdout.close()
    return_code = popen.wait()
    r = {}
    r["percentComplete"] = f"100%"
    r["word"] = "DONE"
    yield json.dumps(r)


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
