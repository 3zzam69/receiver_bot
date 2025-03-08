from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# نموذج البيانات التي سيتم استقبالها
class UserData(BaseModel):
    name: str
    age: int

@app.post("/receive")
def receive_data(user: UserData):
    print(f"تم استقبال البيانات: {user.name}, العمر: {user.age}")
    return {"message": f"تم استقبال البيانات: {user.name}, العمر: {user.age}"}
