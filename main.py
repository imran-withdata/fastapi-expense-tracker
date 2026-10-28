from fastapi import FastAPI, HTTPException, Path

app = FastAPI()

# File load / load json file
import json # python built in package for jason loaded
def load_data():
    with open('expenses.json', 'r') as f:
        data = json.load(f)
    return data


@app.get("/") # End Point
def view():
    return "Congratulation for Entry"

@app.get("/about")
def view():
    return "This is our about page"


# view all data
@app.get("/view")
def view_expenses():
    data = load_data()
    return data







# view specific data
@app.get("/view/{expense_id}")
def view_expenses(expense_id: str = Path (...,description= "ID of the expense" ,example ='E001')):
    data = load_data()
    if expense_id in data:
        return data[expense_id ]
    else:
        return HTTPException(status_code=404, detail="Expense not found")









# data sort = Ascending & descending order  / Use of Query parameter

@app.get("/sort")
def view_sorted_expenses(sorted_by: str ):
    data = load_data() # load all database

    sorted_data = list(data.values()) # dictionaris values converted to list 
    def get_value(expense):
        return expense[sorted_by]
    sorted_data.sort(key = get_value, reverse=True ) # reverse = True for Descending order
    # sorted_data.sort(key = lambda x: x[sorted_by]) # sort is a built in function of list. Details = 2.17 mint
    return sorted_data





# data sort = Ascending & descending order + select order normally
@app.get("/sorted")
def view_sorted_expenses(sorted_by: str, order: str ):
    data = load_data() # load all database

    sorted_data = list(data.values()) # dictionaris values converted to list 
    def get_value(expense):
        return expense[sorted_by]
    if order == "asc":
        sorted_data.sort(key = get_value) 
    else:
        sorted_data.sort(key = get_value, reverse= True)
    return sorted_data

# call  =    http://127.0.0.1:8000/sort?sorted_by=amount&order=desc






    # Use of (post endpoint / request) for create. Add new data. details:2.35 mint


from pydantic import BaseModel, Field
from typing import Annotated, Optional

class Expense(BaseModel):
    id: Annotated[str, Field(...,description= "ID of the expense" ,example ='E001')]
    name: Annotated[str, Field(...,description= "Name of the expense" ,example ='Lunch')]
    amount:Annotated[int, Field(...,description= "Amount of the expense" ,example ='500')]
    category:Annotated[str, Field(...,description= "Category of the expense" ,example ='Food')]
    date:Annotated[str, Field(...,description= "Date of the expense" ,example ='2026-08-16')]
    description:Annotated[str, Field(...,description= "Description of the expense" ,example ='Lunch at a local restaurant')]



@app.post("/create")
def create_expense(expense : Expense):
    data = load_data()
    if expense.id in data: # for duplicate data remove
        raise HTTPException(status_code = 400, detail= "Expense id already exist")
    data[expense.id] = expense.model_dump(exclude=['id']) # Add new data & exclude id
    save_data(data)


   # Save file
def save_data(data):
    with open('expenses.json','w') as f:    
        json.dump(data,f)











 # Use of put request / Update something


# class Expense_update(BaseModel):
    # Optional[str] means that the value of the field can be either a string or None.
    # name: Annotated[Optional[str], Field(default= None)]
    # amount:Annotated[Optional[int], Field(default= None)]
    # category:Annotated[Optional[str], Field(default= None)]
    # date:Annotated[Optional[str], Field(default= None)]
    # description:Annotated[Optional[str], Field(default= None)]

# same work
class Expense_update(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None


@app.put("/edit/{expense_id}")
def Update_expense(expense : Expense_update, expense_id : str):
    data = load_data()
    if expense_id not in data: # if expense_id not in data:
        raise HTTPException(status_code = 404, detail= "Expense not found")
    update_data = expense.model_dump(exclude_unset=True) # Update for Data
    data[expense_id].update(update_data)
    save_data(data)







# Delete expense endpoint


@app.delete("/delete/{expense_id}")
def Delete_expense(expense_id: str):
    data = load_data()
    if expense_id not in data:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    del data[expense_id]
    save_data(data)
    # Successful response return
    return {"message": "Expense deleted successfully", "deleted_id": expense_id}

