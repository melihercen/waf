from fastapi import FastAPI

app=FastAPI()

@app.get("/")
async def home():
    return {
        "message":"Backend çalışıyor"
    }

@app.put("/user")
async def update_user():
    return{
        "message":"Put çalıştı."
    }