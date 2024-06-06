from fastapi import FastAPI
from src.routers import emp_gen_info


app = FastAPI()


app.include_router(
    emp_gen_info.router,
    tags=['store general info']
)