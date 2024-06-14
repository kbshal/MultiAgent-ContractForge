from fastapi import FastAPI
from src.routers import emp_gen_info
import uvicorn
from fastapi.middleware.cors import CORSMiddleware



origins = [
    "*",
]



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    emp_gen_info.router,
    tags=['store general info']
)


if __name__ == "__main__":
    uvicorn.run("main:app", 
    host="0.0.0.0", 
    port=29349, 
    reload=True
    )