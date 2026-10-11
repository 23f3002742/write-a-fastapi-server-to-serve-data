from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

import pandas as pd

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

df = pd.read_csv("q-fastapi.csv")
df["studentId"] = df["studentId"].astype(int)
df["class"] = df["class"].astype(str)


@app.get("/api")
async def get_students(class_: Optional[List[str]] = Query(None, alias="class")):
    if class_ is None or len(class_) == 0:
        filtered = df
    else:
        filtered = df[df["class"].isin(class_)]
    students = [
        {"studentId": int(row["studentId"]), "class": str(row["class"])}
        for _, row in filtered.iterrows()
    ]
    return {"students": students}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
