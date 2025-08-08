from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import tempfile
import os
import pandas as pd
import matplotlib.pyplot as plt
import base64
import io

app = FastAPI()

@app.post("/api/")
async def analyze(
    questions: UploadFile = File(...),
    files: list[UploadFile] = File(default=[])
):
    # Read the questions.txt
    questions_text = (await questions.read()).decode("utf-8")

    # Save uploaded files temporarily
    temp_dir = tempfile.mkdtemp()
    file_paths = {}
    for f in files:
        path = os.path.join(temp_dir, f.filename)
        with open(path, "wb") as out:
            out.write(await f.read())
        file_paths[f.filename] = path

    # Here’s where your custom LLM/data logic goes.
    # For now, we’ll just mock a sample Wikipedia example output.
    # Replace this with actual scraping + analysis.
    answers = [
        1,  # Q1 answer
        "Titanic",  # Q2
        0.485782,  # Q3
        generate_sample_plot_base64()  # Q4
    ]

    return JSONResponse(content=answers)


def generate_sample_plot_base64():
    # Dummy scatterplot with red dotted regression line
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 5, 4, 5]

    plt.figure()
    plt.scatter(x, y)
    plt.plot(x, y, "r--")
    plt.xlabel("Rank")
    plt.ylabel("Peak")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode("utf-8")
