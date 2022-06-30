from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Union

from market.symbol import Stock
from settings import DOM_STOCK_DATA
from web.model import SymbolRate
from web.service import RateService

app = FastAPI()
rate_service= RateService()


class RequestRate(BaseModel):
    symbols: List[str] = []
    date: Union[str, None] = None
    count: int = 0


class ResponseRate(BaseModel):
    item: Dict[str, SymbolRate]


@app.get("/")
async def read_root():
    return {"msg": "Hello World"}


@app.get("/rate/domstock")
async def get_domstock_rate(req: RequestRate):
    symbols = [Stock(s) for s in req.symbols]
    item = rate_service.daily_rate(
        model=DOM_STOCK_DATA,
        symbols=symbols,
        date=req.date,
        count=req.count)

    response = {
        "item": item
    }
    return response
