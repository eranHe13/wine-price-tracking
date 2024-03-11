import sys
from pathlib import Path
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import crud_api

app = FastAPI()



# Setup CORS
origins = [
    "http://localhost:3000",  # Assuming your React app runs on this port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login/")
async def check_log_in(userData: dict = Body(...)):
    res = crud_api.get_user_login_details(userData["email"], userData["password"])
    print("enterd check log in")
    print(res)
    if res:
        return {"user": res}
    else:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    

@app.post("/details/")
async def get_user_details(userID: dict = Body(...)):
    print("userID: ", userID["userID"])
    res = crud_api.get_user_wine_list(userID["userID"])
    if res:        return { "data" :res}
    else:
        raise HTTPException(status_code=401, detail="no products found")


@app.post("/removeWine/")
async def remove_wine_for_user(data: dict = Body(...)):
    print("entered remove_wine_for_user")
    res = crud_api.remove_wine_for_user_by_user_id(data["user_id"], data["product_id"])
    
@app.post("/addwine/")
async def get_user_details(data: dict = Body(...)):
    print("data: ", data)
    res = crud_api.add_new_product_for_user(data["user_id"], data["wine_name"], data["price"])
    
    
    
    
    
@app.post("/register/")
async def register(userData: dict = Body(...)):
    print("regisiter start")
    res = crud_api.add_user(userData["username"], userData["password"] ,userData["email"] )
    if res : return res
    else : return None

    
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

#python -m uvicorn server:app --reload
