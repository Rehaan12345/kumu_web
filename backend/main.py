from fastapi import FastAPI
import os
from dotenv import load_dotenv
from spreadsheet import get_values, update_values
import google.auth
from typing import List
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

class Values(BaseModel):
    vals: List[str]

@app.get("/")
def home():
    return {"data": "rehaan"}

@app.get("/getvals")
def get_vals():
    return get_values()

# Length of values list can be as many, as long as values[0] is always the "FROM" element, it can have as many "TO" elements as it wants
# Row should always be the last row (updates to (row - 1)).
    # Maybe update later, in the UI (SvelteKitJS) or spreadsheet.py file, for convenience, etc.
# If updating "TO" element, update columnIndex to 1.
@app.post("/updatevals/")
def update_vals(values: Values, row: int, col_ind: int):
    return update_values(values.vals, row, 0)