from fastapi import FastAPI, File, UploadFile
import shutil
import json

from .fin.fundamentus_stocks import get_data as get_stocks_data
from .fin.fundamentus_fii import get_data as get_fii_data
from datetime import datetime

app = FastAPI()

stocks, fii = dict(get_stocks_data()), dict(get_fii_data())
dia = datetime.strftime(datetime.today(), '%d')
stocks = {outer_k: {inner_k: float(inner_v) for inner_k, inner_v in outer_v.items()} for outer_k, outer_v in stocks.items()}
fii = {outer_k: {inner_k: float(inner_v) for inner_k, inner_v in outer_v.items()} for outer_k, outer_v in fii.items()}


@app.get("/api")
async def read_root():
    return {"message": "Hello, world!"}


@app.get("/api/fin/stocks")
async def getFinStocks():
    global stocks, dia
    
    # Then only update once a day
    if dia == datetime.strftime(datetime.today(), '%d'):
        return stocks
    else:
        stocks, dia = dict(get_stocks_data()), datetime.strftime(datetime.today(), '%d')
        stocks = {outer_k: {inner_k: float(inner_v) for inner_k, inner_v in outer_v.items()} for outer_k, outer_v in stocks.items()}
        return stocks


@app.get("/api/fin/fii")
async def getFinFii():
    global fii, dia
    
    # Then only update once a day
    if dia == datetime.strftime(datetime.today(), '%d'):
        return fii
    else:
        fii, dia = dict(get_fii_data()), datetime.strftime(datetime.today(), '%d')
        fii = {outer_k: {inner_k: float(inner_v) for inner_k, inner_v in outer_v.items()} for outer_k, outer_v in fii.items()}
        return fii

@app.get("/api/fin/fundsexplorer")
def get_fii():
    with open('db/fii.json', 'r') as file:
        data = json.load(file)
        return data

@app.put("/api/fin/fundsexplorer")
async def create_upload_file(file: UploadFile):
    with open("db/fii.json", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}
