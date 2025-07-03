from fastapi import FastAPI

from api.routes import interviews, results, signaling, auth, agents

app = FastAPI()


app.include_router(results.router, prefix="/api")
app.include_router(signaling.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(agents.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Video AI System API"}
