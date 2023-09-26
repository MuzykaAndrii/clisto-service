from fastapi import FastAPI


app = FastAPI(
    title="Clisto service",
)

@app.get("/ping/")
async def pong():
    return {"response": "pong"}