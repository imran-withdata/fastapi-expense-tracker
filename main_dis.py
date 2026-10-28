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

"""
পাথ বা ইউআরএল (/view/{expense_id})
/view/: এটি হলো ওয়েবসাইটের মূল ঠিকানার পরের একটি অংশ (রুট বা পাথ)। যেমন: http://localhost:8000/view/।

{expense_id} (থার্ড ব্র্যাকেটের ভেতরে): এটি হলো একটি ডাইনামিক বা পরিবর্তনশীল অংশ (Path Parameter)। এর ভেতরে নির্দিষ্ট কোনো আইডি লেখা থাকে না, বরং ব্যবহারকারী যে আইডি দেখতে চান সেটি বসে যায়।

যেমন: কেউ যদি দেখতে চান  E003 আইডিওয়ালা খরচটি, তখন ইউআরএল হবে: /view/E003

আবার কেউ যদি দেখতে চান abc আইডিওয়ালা খরচটি, তখন ইউআরএল হবে: /view/abc

এই {expense_id} এর ভেতরে যা-ই লেখা হোক না কেন, FastAPI সেটিকে একটি ভেরিয়েবলের মতো ধরে নিচের পাইথন ফাংশনে পাঠিয়ে দেয়, যাতে সেই আইডি ধরে ডাটাবেস বা ফাইল থেকে ওই নির্দিষ্ট খরচটি খুঁজে বের করা যায়।

"""
"""
ব্র্যাকেটের ভেতরের অংশ (expense_id: str):
expense_id: এটি হলো একটি প্যারামিটার বা আর্গুমেন্ট (Parameter)। ইউআরএল থেকে যে আইডিটি পাঠানো হবে, তা এই ভেরিয়েবলের ভেতরে এসে জমা হবে।

: str (টাইপ হিন্ট বা Type Hint): পাইথনে এটি বাধ্যতামূলক নয়, তবে এটি দিয়ে বোঝানো হয়েছে যে expense_id-এর মানটি আবশ্যিকভাবে একটি স্ট্রিং (str) বা টেক্সট ফরম্যাটে আসবে।

"""
"""
return data[expense_id ] লিখে ওই নির্দিষ্ট আইডির বিপরীতে থাকা খরচের সমস্ত বিস্তারিত তথ্য (যেমন: টাকার পরিমাণ, ক্যাটাগরি, তারিখ ইত্যাদি) ডিকশনারি থেকে বের করে আনা হয়।
"""

"""
Path Parameter
FastAPI-তে path Parameter কীভাবে কাজ করে?
FastAPI-তে পাথ প্যারামিটার ডিফাইন করতে সেকেন্ড ব্র্যাকেট বা কার্লি ব্রেস { } ব্যবহার করা হয়।

ইউআরএলে যখন {expense_id} লেখা হয়, তখন FastAPI বুঝে নেয় যে ব্যবহারকারী /view/-এর পরে যা-ই লিখবেন, সেটি একটি চলক বা ভেরিয়েবলের মতো কাজ করবে।

ব্র্যাকেটের ভেতরের নাম (expense_id) এবং আপনার পাইথন ফাংশনের প্যারামিটারের নাম (expense_id: str) হুবহু এক হতে হবে। তাহলেই FastAPI ইউআরএল থেকে ওই মানটি স্বয়ংক্রিয়ভাবে এনে ফাংশনের ভেতরে পাঠিয়ে দেবে।

"""









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

"""
def view_sorted_expenses(sorted_by: str ):
এখানে sorted_by হলো একটি কোয়েরি প্যারামিটার (Query Parameter)।
উদাহরণস্বরূপ, ব্যবহারকারী যখন ব্রাউজারে /sort?sorted_by=amount এভাবে লিখবেন, তখন sorted_by-এর মান হয়ে যাবে "amount"। অর্থাৎ, কোন ফিল্ড বা বিষয়ের ওপর ভিত্তি করে সর্ট করা হবে, তা এখানে বলে দেওয়া হয়।

sorted_data = list(data.values()) # dictionaris values converted to list
ডিকশনারি সরাসরি সর্ট করা একটু জটিল, তাই data.values() দিয়ে শুধু খরচের ডিকশনারিগুলোর মান বের করে সেগুলোকে একটি পাইথন লিস্টে (list) রূপান্তর করা হয়েছে।

def get_value(expense):
        return expense[sorted_by]
পাইথনের সর্ট ফাংশনকে বুঝিয়ে দেওয়ার জন্য যে কোন ফিল্ড ধরে সর্ট করতে হবে, এই ছোট ফাংশনটি তৈরি করা হয়েছে। এটি প্রতিটি খরচের রেকর্ড (expense) থেকে sorted_by অনুযায়ী নির্দিষ্ট মানটি বের করে দেয় (যেমন: খরচের অ্যামাউন্ট বা ক্যাটাগরি)।

sorted_data.sort(key = get_value, reverse=True ) # reverse = True for Descending order
.sort(): এটি লিস্টের একটি বিল্ট-ইন মেথড যা লিস্টকে সাজায়।

key = get_value: এটি পাইথনকে বলে দেয় যে get_value ফাংশন থেকে পাওয়া মানের ওপর ভিত্তি করে সর্টিং করতে হবে।

reverse=True: এর অর্থ হলো সাজানোর ক্রমটি হবে বড় থেকে ছোট (Descending order) বা সর্বোচ্চ থেকে সর্বনিম্ন। (যদি ছোট থেকে বড় বা Ascending করতে চান, তবে এটি False রাখতে হবে বা তুলে দিতে হবে)।

(নিচের কমেন্ট করা লাইনটিতে # sorted_data.sort(key = lambda x: x[sorted_by]) দেখানো হয়েছে যে, এই একই কাজ আলাদা ছোট ফাংশন না বানিয়ে এক লাইনে lambda ফাংশন ব্যবহার করেও করা সম্ভব।)


return sorted_data
সবশেষে, সাজানো বা সর্ট করা সম্পূর্ণ লিস্টটি রেসপন্স হিসেবে ক্লায়েন্ট বা ব্রাউজারে ফিরিয়ে দেওয়া হয়।

"""



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

"""
def view_sorted_expenses(sorted_by: str, order: str ):
এখানে দুটি কোয়েরি প্যারামিটার ব্যবহার করা হয়েছে:
sorted_by: কোন ফিল্ড বা বিষয়ের ওপর ভিত্তি করে সর্ট করা হবে (যেমন: amount বা date)।
order: কোন ক্রমে সাজানো হবে (যেমন: ছোট থেকে বড় অর্থাৎ asc, বা বড় থেকে ছোট অর্থাৎ অন্য কিছু)।
ব্রাউজারে ইউআরএলটি দেখতে এমন হতে পারে: /sorted?sorted_by=amount&order=asc


data = load_data() # load all database
    sorted_data = list(data.values()) # dictionaris values converted to list
load_data() দিয়ে সমস্ত ডেটা লোড করা হয় এবং data.values() দিয়ে ডিকশনারির মানগুলোকে একটি লিস্টে (list) রূপান্তর করা হয়, যাতে সহজেই সর্ট করা যায়।


def get_value(expense):
        return expense[sorted_by]
এই ছোট ফাংশনটি প্রতিটি খরচের রেকর্ড থেকে sorted_by অনুযায়ী নির্দিষ্ট মানটি বের করে দেয়।



if order == "asc":
        sorted_data.sort(key = get_value) 
    else:
        sorted_data.sort(key = get_value, reverse= True)
 
if order == "asc":: যদি ব্যবহারকারী order-এর মান asc (ascending বা ছোট থেকে বড়) দেন, তবে স্বাভাবিক নিয়মে .sort(key = get_value) রান হবে (ছোট থেকে বড় সাজানোর জন্য)।

else:: যদি asc ছাড়া অন্য কিছু দেওয়া হয় (যেমন: desc), তখন reverse=True কাজ করবে এবং ডেটাগুলো বড় থেকে ছোট (Descending order) ক্রমানুসারে সাজানো হবে।


return sorted_data
return sorted_data

"""




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

"""
BaseModel: Pydantic-এর মূল ক্লাস। যেকোনো ডেটা মডেল তৈরি করতে হলে এই ক্লাসটিকে ইনহেরিট (Inherit) করতে হয়। এটি স্বয়ংক্রিয়ভাবে ইনপুট ডেটা চেক করে দেখে ডেটা টাইপ ঠিক আছে কি না।

Field: ফিল্ডের ভেতরে বিভিন্ন অতিরিক্ত তথ্য (যেমন: বিবরণ, উদাহরণ, বা ভ্যালিডেশন রুলস) যুক্ত করার জন্য এটি ব্যবহার করা হয়।

Annotated: এটি পাইথনের একটি আধুনিক ফিচার (typing মডিউল থেকে আসা), যার মাধ্যমে কোনো ডেটা টাইপের সাথে মেটাডেটা (যেমন Field(...)) যুক্ত করা যায়।

class Expense(BaseModel):
এখানে Expense নামের একটি ক্লাস তৈরি করা হয়েছে যা BaseModel-কে অনুসরণ করে। এর ভেতরে খরচের সাথে সম্পর্কিত সমস্ত ফিল্ড বা প্রপার্টি ডিফাইন করা হয়েছে।


এই মডেলের সুবিধা কী?
ডেটা ভ্যালিডেশন: ব্যবহারকারী যদি amount-এর জায়গায় কোনো লেখা বা ভুল ডেটা পাঠান, তখন Pydantic সাথে সাথে এরর ধরে ফেলবে এবং রিকোয়েস্ট রিজেক্ট করবে।

অটো ডকুমেন্টেশন: FastAPI-এর /docs পেজে এই মডেলটি ব্যবহার করার ফলে প্রতিটি ফিল্ডের পাশে description এবং example সুন্দরভাবে দেখা যায়, যা API ব্যবহার করা ডেভেলপারদের জন্য অনেক সহজ করে দেয়।


"""

@app.post("/create")
def create_expense(expense : Expense):
    data = load_data()
    if expense.id in data: # for duplicate data remove
        raise HTTPException(status_code = 400, detail= "Expense id already exist")
    data[expense.id] = expense.model_dump(exclude=['id']) # Add new data & exclude id
    save_data(data)

"""
১. রাউট ডেকোরেটর (POST Method)
@app.post("/create")
এটি একটি FastAPI POST রাউট। ব্যবহারকারী যখন কোনো নতুন ডেটা সার্ভারে পাঠাতে চান (যেমন: নতুন খরচ এন্ট্রি করা), তখন POST মেথড ব্যবহার করা হয়। /create লিংকে রিকোয়েস্ট পাঠালে এই ফাংশনটি রান হবে।

২. ফাংশন ডিফিনিশন এবং রিকোয়েস্ট বডি
def create_expense(expense : Expense):
এখানে ইনপুট হিসেবে আগের তৈরি করা Expense (Pydantic মডেল) ব্যবহার করা হয়েছে। ব্যবহারকারী যখন রিকোয়েস্ট পাঠাবেন, FastAPI স্বয়ংক্রিয়ভাবে সেই ডেটা চেক করবে এবং expense অবজেক্টের মধ্যে গুছিয়ে রাখবে।

৩. ডাটা লোড করা
data = load_data()
আগের মতো load_data() ফাংশন দিয়ে বর্তমান সমস্ত খরচের রেকর্ডগুলো লোড করে data ভেরিয়েবলে রাখা হয়।


৪. ডুপ্লিকেট চেক বা যাচাই করা
if expense.id in data: # for duplicate data remove
        raise HTTPException(status_code = 400, detail= "Expense id already exist")

if expense.id in data:: এখানে চেক করা হচ্ছে নতুন যে আইডি দিয়ে খরচ যোগ করা হচ্ছে, সেই একই আইডিওয়ালা কোনো খরচ আগে থেকেই ডাটাবেসে আছে কি না।
raise HTTPException(...): যদি আইডিটি আগেই থেকে থাকে, তবে কোডটি ফাস্টিএপিআই-এর HTTPException-এর মাধ্যমে 400 Bad Request স্ট্যাটাস কোড এবং "Expense id already exist" মেসেজ রিটার্ন করে রিকোয়েস্টটি বাতিল করে দেয়। এর ফলে একই আইডি দুইবার এন্ট্রি হতে পারে না।


৫. নতুন ডেটা যুক্ত করা এবং আইডি বাদ দেওয়া
data[expense.id] = expense.model_dump(exclude=['id']) # Add new data & exclude id

data[expense.id] = ...: ডিকশনারির ভেতর ওই নির্দিষ্ট expense.id-কে কী (Key) হিসেবে সেট করা হচ্ছে।
expense.model_dump(exclude=['id']): পড্যানটিক মডেলের এই মেথডটি দিয়ে পুরো ডেটাকে পাইথন ডিকশনারিতে রূপান্তর করা হয়। তবে exclude=['id'] ব্যবহারের কারণে ডিকশনারির ভেতরের ভ্যালু থেকে id ফিল্ডটি বাদ দেওয়া হয়।
কেন বাদ দেওয়া হয়? যেহেতু expense.id ইতিমধ্যেই ডিকশনারির প্রধান key হিসেবে ব্যবহার করা হচ্ছে, তাই ভ্যালুর ভেতরে আবার id রাখার দরকার নেই (এতে ডেটা রিডানডেন্সি বা ডাবল এন্ট্রি এড়ানো যায়)।


৬. ডেটা সেভ করা
save_data(data)
সবশেষে, নতুন খরচটি যুক্ত করার পর পরিবর্তিত সম্পূর্ণ data ডিকশনারিটি save_data(data) ফাংশনের মাধ্যমে ফাইল বা ডাটাবেসে স্থায়ীভাবে সংরক্ষণ (Save) করা হয়।

"""


   # Save file
def save_data(data):
    with open('expenses.json','w') as f:    
        json.dump(data,f)
"""
এই পাইথন ফাংশনটির মূল কাজ হলো পাইথন কোডের ভেতরে থাকা সমস্ত খরচের ডেটা বা রেকর্ডগুলোকে একটি ফাইলে (যেমন: expenses.json) স্থায়ীভাবে সংরক্ষণ বা সেভ (Save) করা।

১. ফাংশন ডিফিনিশন (Function Definition)
def save_data(data):
save_data নামের এই ফাংশনটি একটি আর্গুমেন্ট বা প্যারামিটার (data) গ্রহণ করে। এই data-র ভেতরে সমস্ত খরচের ডিকশনারি বা রেকর্ডগুলো জমা থাকে, যা ফাইলে সেভ করতে হবে।

২. ফাইল ওপেন করা (Context Manager)
with open('expenses.json','w') as f:

open('expenses.json', 'w'): এখানে expenses.json নামের ফাইলটি রাইট মোডে ('w') ওপেন করা হচ্ছে। রাইট মোডের কাজ হলো ফাইলটি যদি আগে থেকে না থাকে তবে নতুন তৈরি করা, আর যদি থাকে তবে আগের পুরনো ডেটা মুছে নতুন ডেটা সেখানে লেখা।
with: পাইথনে ফাইল নিয়ে কাজ করার সময় with ব্যবহার করা একটি চমৎকার প্র্যাকটিস। এর সুবিধা হলো, ফাইলের ভেତরের কাজ শেষ হওয়ামাত্র এটি স্বয়ংক্রিয়ভাবে ফাইলটি বন্ধ (close) করে দেয়, ফলে মেমোরি লিক বা ফাইল করাপ্ট হওয়ার ঝুঁকি থাকে না।
as f: ফাইলটিকে একটি হ্যান্ডলার বা ভেরিয়েবল f-এর ভেতরে রাখা হয়, যাতে পরবর্তীতে ফাইলে ডেটা লেখা যায়।


৩. JSON ফরম্যাটে ডেটা লেখা
json.dump(data,f)
json.dump(): এটি পাইথনের বিল্ট-ইন json মডিউলের একটি ফাংশন। এর মূল কাজ হলো পাইথনের নিজস্ব ডেটা স্ট্রাকচার (যেমন: ডিকশনারি বা লিস্ট) ডেটাকে JSON ফরম্যাটে রূপান্তর করে সরাসরি নির্দিষ্ট ফাইলে (f-এর মাধ্যমে) লিখে ফেলা।

সংক্ষেপে: এই ফাংশনটি আপনার অ্যাপের মেমোরিতে থাকা সমস্ত খরচের রেকর্ডগুলো গুছিয়ে expenses.json ফাইলের মধ্যে পার্মানেন্টলি বা স্থায়ীভাবে সেভ করে রাখে, যাতে পরবর্তীতে অ্যাপ রিস্টার্ট হলেও ডেটা হারিয়ে না যায়।

"""










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

"""
এই পাইথন কোডটিতে Pydantic ব্যবহার করে একটি **`Expense_update`** মডেল তৈরি করা হয়েছে। এটি সাধারণত কোনো বিদ্যমান খরচ (Expense) আপডেট বা পরিবর্তন করার সময় (`PATCH` বা `PUT` রিকোয়েস্টে) ব্যবহার করা হয়।

কোডটির বিস্তারিত ব্যাখ্যা নিচে দেওয়া হলো:

### ১. এই মডেলের উদ্দেশ্য কী?

নতুন খরচ তৈরি করার সময় (`POST` রিকোয়েস্টে) সব তথ্য (যেমন: নাম, অ্যামাউন্ট, ক্যাটাগরি ইত্যাদি) দেওয়া বাধ্যতামূলক থাকে। কিন্তু কোনো পুরনো খরচ **আপডেট** করার সময় ব্যবহারকারী হয়তো শুধু একটি নির্দিষ্ট তথ্য বদলাতে চাইতে পারেন (যেমন: শুধু নাম বা শুধু টাকার পরিমাণ)। পুরো ফর্ম আবার পূরণ করার প্রয়োজন নেই। এই ধরনের আংশিক আপডেট (Partial Update)-এর জন্যই এই `Expense_update` মডেলটি তৈরি করা হয়েছে।

### ২. লাইন-বাই-লাইন ব্যাখ্যা:

* **`class Expense_update(BaseModel):`**
* এটি একটি নতুন Pydantic মডেল ক্লাস, যা আপডেটের ডেটা ভ্যালিডেশন করার জন্য তৈরি করা হয়েছে। (লক্ষ্য করুন, এখানে `id` রাখা হয়নি, কারণ আইডি দিয়ে আগেই রেকর্ডটি খুঁজে বের করা হয়েছে)।


* **`name: Optional[str] = None`**
* **`Optional[...]`**: টাইপিং মডিউল থেকে আসা এই কিওয়ার্ডটি দিয়ে বোঝানো হয় যে এই ফিল্ডটি বাধ্যতামূলক নয় (Optional)।
* **`= None`**: যদি ব্যবহারকারী আপডেট করার সময় `name` পরিবর্তন করতে না চান এবং ফিল্ডটি ফাঁকা রাখেন, তবে এর ডিফল্ট মান হয়ে যাবে `None`।


* **`amount: Optional[float] = None`**
* খরচের পরিমাণ আপডেটের জন্য। এখানে ডেটা টাইপ `float` (দশমিক সংখ্যা বা পূর্ণসংখ্যা উভয়ের জন্য উপযোগী) দেওয়া হয়েছে এবং এটিও অপশনাল (`= None`) রাখা হয়েছে।


* **বাকি ফিল্ডগুলো (`category`, `date`, `description`):**
* এগুলোর ক্ষেত্রেও একই নিয়ম প্রযোজ্য। ব্যবহারকারী যদি ক্যাটাগরি, তারিখ বা বিবরণ বদলাতে চান, তবে পাঠাতে পারেন; না পাঠালে এগুলো `None` হিসেবে গণ্য হবে এবং আগের ডেটা অপরিবর্তিত থাকবে।



**সংক্ষেপে:** এই মডেলটি নিশ্চিত করে যে, আপডেট রিকোয়েস্টে ব্যবহারকারী যে ফিল্ডগুলো পাঠাবেন কেবল সেগুলোর ডেটায় পরিবর্তন আসবে, আর বাকি ফিল্ডগুলো আগের মতোই থেকে যাবে।

"""
@app.put("/edit/{expense_id}")
def Update_expense(expense : Expense_update, expense_id : str):
    data = load_data()
    if expense_id not in data: # if expense_id not in data:
        raise HTTPException(status_code = 404, detail= "Expense not found")
    update_data = expense.model_dump(exclude_unset=True) # Update for Data
    data[expense_id].update(update_data)
    save_data(data)

"""
এই পাইথন (FastAPI) কোডটির মূল কাজ হলো ডাটাবেসে থাকা কোনো বিদ্যমান খরচ বা (Expense) এর তথ্য পরিবর্তন বা **আপডেট (Update)** করা (`PUT` রিকোয়েস্টের মাধ্যমে)।

কোডটির লাইন-বাই-लाइन বিস্তারিত ব্যাখ্যা নিচে দেওয়া হলো:

### ১. রাউট ডেকোরেটর (`PUT` মেথড)

```python
@app.put("/edit/{expense_id}")

```

* এটি একটি FastAPI `PUT` রাউট। সাধারণত কোনো পুরনো ডেটা পরিবর্তন বা আপডেট করার জন্য `PUT` মেথড ব্যবহার করা হয়।
* এখানে `/edit/{expense_id}` লিংকে রিকোয়েস্ট পাঠানো হয়, যেখানে `{expense_id}` হলো একটি পাথ প্যারামিটার যা বলে দেয় কোন খরচটি পরিবর্তন করতে হবে।

### ২. ফাংশন ডিফিনিশন এবং প্যারামিটার

```python
def Update_expense(expense : Expense_update, expense_id : str):

```

* এই ফাংশনটি দুটি প্রধান ইনপুট গ্রহণ করে:
1. **`expense : Expense_update`**: ব্যবহারকারী যে নতুন বা পরিবর্তিত তথ্যগুলো পাঠাবেন, তা `Expense_update` মডেল অনুযায়ী রিকোয়েস্ট বডি থেকে আসবে।
2. **`expense_id : str`**: ইউআরএল থেকে আসা সেই নির্দিষ্ট আইডির মান, যা আপডেট করা হবে।



### ৩. ডাটা লোড করা

```python
    data = load_data()

```

* `load_data()` ফাংশন দিয়ে বর্তমান সমস্ত খরচের রেকর্ডগুলো ফাইল বা ডাটাবেস থেকে লোড করে `data` ভেরিয়েবলে রাখা হয়।

### ৪. আইডি চেক বা অস্তিত্ব যাচাই (404 Error Handling)

```python
    if expense_id not in data: 
        raise HTTPException(status_code = 404, detail= "Expense not found")

```

* **`if expense_id not in data:`**: চেক করা হচ্ছে ব্যবহারকারী যে আইডি দিয়ে আপডেট করতে চাচ্ছেন, সেটি আদেও ডাটার মধ্যে আছে কি না।
* **`raise HTTPException(...)`**: যদি আইডিটি না পাওয়া যায়, তবে ফাস্টএপিআই-এর মাধ্যমে **`404 Not Found`** স্ট্যাটাস কোড এবং `"Expense not found"` মেসেজ রিটার্ন করে কোডটি থামিয়ে দেওয়া হয়।

### ৫. শুধু পরিবর্তিত ডেটা ফিল্টার করা (`exclude_unset=True`)

```python
    update_data = expense.model_dump(exclude_unset=True) # Update for Data

```

* এই লাইনটি অত্যন্ত গুরুত্বপূর্ণ! `exclude_unset=True` ব্যবহার করার ফলে পড্যানটিক মডেল চেক করে দেখে ব্যবহারকারী কোন কোন ফিল্ডের মান পরিবর্তন করার জন্য পাঠিয়েছেন।
* উদাহরণস্বরূপ: ব্যবহারকারী যদি শুধু `amount` বদলাতে চান এবং বাকি ফিল্ডগুলো ফাঁকা রাখেন, তবে শুধু `amount`-এর ডেটাই `update_data`-র ভেতরে আসবে, বাকি অপশনাল ফিল্ডগুলো বাদ (`exclude`) হয়ে যাবে।

### ৬. ডেটা আপডেট বা মার্জ করা

```python
    data[expense_id].update(update_data)

```

* পাইথন ডিকশনারির `.update()` মেথড ব্যবহার করে নির্দিষ্ট `expense_id`-এর পুরনো ডেটার সাথে নতুন পরিবর্তিত `update_data` যুক্ত করে দেওয়া হয়। ফলে যে ফিল্ডগুলো পরিবর্তন করা হয়েছে শুধু সেগুলো বদলে যায়, আর বাকিগুলো আগের মতোই থাকে।

### ৭. ডেটা স্থায়ীভাবে সেভ করা

```python
    save_data(data)

```

* পরিশেষে, আপডেট হওয়া সম্পূর্ণ ডিকশনারিটি `save_data(data)` ফাংশনের মাধ্যমে পুনরায় ফাইলে (যেমন: `expenses.json`) পার্মানেন্টলি সেভ করে দেওয়া হয়।


"""













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


"""
এই পাইথন (FastAPI) কোডটির মূল কাজ হলো সিস্টেমে থাকা নির্দিষ্ট কোনো খরচ বা (Expense) রেকর্ড আইডি ধরে চিরতরে **মুছে ফেলা বা ডিলিট করা** (`DELETE` রিকোয়েস্টের মাধ্যমে)।

কোডটির লাইন-বাই-লাইন বিস্তারিত ব্যাখ্যা নিচে দেওয়া হলো:

### ১. রাউট ডেকোরেটর (`DELETE` মেথড)

```python
@app.delete("/delete/{expense_id}")

```

* এটি একটি FastAPI `DELETE` রাউট। সাধারণত সার্ভার থেকে কোনো ডেটা মুছে ফেলার জন্য `DELETE` মেথড ব্যবহার করা হয়।
* `/delete/{expense_id}` লিংকে রিকোয়েস্ট পাঠানো হলে এই ফাংশনটি রান হয়, যেখানে `{expense_id}` হলো একটি পাথ প্যারামিটার যা নির্ধারণ করে কোন খরচটি ডিলিট করতে হবে।

### ২. ফাংশন ডিফিনিশন এবং প্যারামিটার

```python
def Delete_expense(expense_id: str):

```

* `Delete_expense` নামের এই ফাংশনটি ইউআরএল থেকে `expense_id` (যা একটি স্ট্রিং বা `str`) গ্রহণ করে।

### ৩. ডাটা লোড করা

```python
    data = load_data()

```

* `load_data()` ফাংশন দিয়ে বর্তমান সমস্ত খরচের রেকর্ডগুলো ফাইল বা ডাটাবেস থেকে লোড করে `data` ভেরিয়েবলে নিয়ে আসা হয়।

### ৪. আইডি চেক বা অস্তিত্ব যাচাই (404 Error Handling)

```python
    if expense_id not in data:
        raise HTTPException(status_code=404, detail="Expense not found")

```

* **`if expense_id not in data:`**: এখানে চেক করা হচ্ছে ব্যবহারকারী যে আইডিটি ডিলিট করতে চাচ্ছেন, সেটি আদেও ডাটার মধ্যে বিদ্যমান আছে কি না।
* **`raise HTTPException(...)`**: যদি আইডিটি না পাওয়া যায়, তবে ফাস্টএপিআই-এর মাধ্যমে **`404 Not Found`** স্ট্যাটাস কোড এবং `"Expense not found"` মেসেজ রিটার্ন করে কোডটি থামিয়ে দেওয়া হয়, যাতে ভুলের কারণে অপ্রয়োজনীয় এরর না ঘটে।

### ৫. ডেটা মুছে ফেলা (`del`)

```python
    del data[expense_id]

```

* পাইথনের বিল্ট-ইন **`del`** কিওয়ার্ড ব্যবহার করে ডিকশনারির নির্দিষ্ট কি (Key) অর্থাৎ `expense_id`-সহ তার সম্পূর্ণ ভ্যালু বা খরচের রেকর্ডটি `data` ডিকশনারি থেকে পাকাপাকিভাবে মুছে ফেলা হয়।

### ৬. ডেটা স্থায়ীভাবে সেভ করা

```python
    save_data(data)

```

* ডিলিট করার পর পরিবর্তিত ডিকশনারিটি `save_data(data)` ফাংশনের মাধ্যমে পুনরায় ফাইলে (যেমন: `expenses.json`) সেভ করে দেওয়া হয়, যাতে পরবর্তীতে অ্যাপ রিস্টার্ট হলেও মুছে ফেলা ডেটা আর ফিরে না আসে।

### ৭. সফলতার বার্তা রিটার্ন করা

```python
    return {"message": "Expense deleted successfully", "deleted_id": expense_id}

```

* অপারেশন সফলভাবে সম্পন্ন হওয়ার পর ক্লায়েন্ট বা ব্রাউজারে একটি JSON রেসপন্স পাঠানো হয়, যেখানে একটি কনফার্মেশন মেসেজ এবং কোন আইডিটি ডিলিট করা হয়েছে (`deleted_id`) তা স্পষ্টভাবে জানিয়ে দেওয়া হয়।
"""
