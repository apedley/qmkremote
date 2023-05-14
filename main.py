from fastapi import FastAPI
from pydantic import BaseModel

from qmkremote import QMKRemote

app = FastAPI()
remote = QMKRemote()

@app.get("/")
async def root():
    status = remote.status()
    if status:
        return {"connected": True, "path": status}
    else:
        return {"connected": False}

@app.get("/matrix/on")
def matrix_on():
    remote.matrix_on()
    return "matrixon"

@app.get("/matrix/off")
def matrix_off():
    remote.matrix_off()
    return "matrixoff"

@app.get("/matrix/indicator/reset")
def matrix_indicator_reset():
    remote.matrix_indicator_reset()
    return "matrixreset"

@app.get("/matrix/indicator/all")
def matrix_indicator_all(q: str | None = None, r: int = 0, g: int = 0, b: int = 0):
    remote.matrix_indicator_all(r, g, b)
    return {"color": {"r": r, "g": g, "b": b}}

@app.get("/matrix/indicator/{start}/{end}")
def matrix_indicator_range(start: int, end: int, q: str | None = None, r: int = 0, g: int = 0, b: int = 0):
    remote.matrix_indicator_range(r, g, b, start, end)
    return {"color": {"r": r, "g": g, "b": b}, "range": {"start": start, "end": end}}