from fastapi import FastAPI
from web_app import models
from web_app.dependencies import engine
from web_app.routes import router


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
