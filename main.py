import datetime

from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError

app = FastAPI(
    title="Trading web app"
)

# Реализация отоброжения ошибок
# @app.exception_handler(ValidationError)
# async def validation_exception_handler(request: Request, exc: ValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors()})
#     )

fake_users = [
    {"id": 1, "role": "admin", "first_name": "Yaroslav", "last_name": "Selivanov"},
    {"id": 2, "role": "investor", "first_name": "John", "last_name": "Jogh"},
    {"id": 3, "role": "trader", "first_name": "Matt", "last_name": "Kac"},
]

fake_users2 = [
    {"id": 1, "role": "admin", "first_name": "Yaroslav", "last_name": "Selivanov"},
    {"id": 2, "role": "investor", "first_name": "John", "last_name": "Jogh"},
    {"id": 3, "role": "trader", "first_name": "Matt", "last_name": "Kac"},
]

fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12},
]


class DegreeType(Enum):
    junior = "junior"
    middle = "middle"
    senior = "senior"


class Degree(BaseModel):
    id: int
    created_at: datetime.datetime
    type_degree: DegreeType  # валидация по имеющимся данным

class User(BaseModel):
    id: int
    role: str
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    degree: Optional[List[Degree]]


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


@app.get("/trades")
def get_trades(limit: int = 1, offset: int = 0):
    return fake_trades[offset:][:limit]


@app.post("/users/{user_id}")
def change_user_name(user_id: int, new_name: str):
    current_user = next((user for user in fake_users if user.get("id") == user_id), None)
    if current_user:
        current_user["first_name"] = new_name
        return {"status": 200, "data": current_user}
    return {"status": 404, "message": "User not found"}


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=10)
    side: str
    price: float = Field(ge=0)  # Больше и равно 0
    amount: float


@app.post("/trades")
def add_trades(trades: List[Trade]):
    for trade in trades:
        fake_trades.append(trade.dict())
    return {
        "status": 200,
        "data": fake_trades,
    }