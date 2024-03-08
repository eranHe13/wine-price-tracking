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
    if res:
        # Assuming you want to return a JSON response with user details
        return {"user": res}
    else:
        # Returning a 401 Unauthorized response for failed login attempts
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    

@app.post("/details/")
async def get_user_details(userID: dict = Body(...)):
    print("userID: ", userID["userID"])
    res = crud_api.get_user_wine_list(userID["userID"])
    if res:
        # Assuming you want to return a JSON response with user details
        return { "data" :res}
    else:
        # Returning a 401 Unauthorized response for failed login attempts
        raise HTTPException(status_code=401, detail="no products found")
    
    
    
    
    
@app.post("/addwine/")
async def get_user_details(data: dict = Body(...)):
    print("data: ", data)
    res = crud_api.add_new_product_for_user(data["user_id"], data["wine_name"], data["price"])
    # if res:
    #     # Assuming you want to return a JSON response with user details
    #     return { "data" :res}
    # else:
    #     # Returning a 401 Unauthorized response for failed login attempts
    #     raise HTTPException(status_code=401, detail="no products found")
    
    
    
    
@app.post("/register/")
async def register(userData: dict = Body(...)):
    print("regisiter start")
    res = crud_api.add_user(userData["username"], userData["password"] ,userData["email"] )
    if res : return res
    else : return None

    
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

#python -m uvicorn server:app --reload
