from routes.AI import router as ai_router
from fastapi import FastAPI


app = FastAPI()

app.include_router(ai_router)



