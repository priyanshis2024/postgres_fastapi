import psycopg2
from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel
from typing import Optional
from psycopg2.extras import RealDictCursor    
import time

app = FastAPI()

class Detail(BaseModel):
    Id: Optional[int] = None
    Name: str
    Domain: str
    Age: int
    Email: str
    Is_student: bool = True
    Rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',password='password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as error:
        print("Database not connected")
        print("Error:", error)
        time.sleep(5)
    
@app.get("/")
def root():
    return {"Welcome to the API!!"}

# Fetching details
@app.get("/details")
def get_posts():
    cursor.execute("SELECT * FROM details")
    posts = cursor.fetchall()
    return posts

# Fetching details by ID
@app.get("/details/{Id}")
def get_post(Id: int):
    cursor.execute('SELECT * FROM details WHERE "Id" = %s', (Id,))
    one_detail = cursor.fetchone()
    print(one_detail)
    if not one_detail:
        raise HTTPException(status_code=404, detail="Detail not found")
    return one_detail

# # Inserting details
@app.post("/details", status_code=status.HTTP_201_CREATED)
def create_post(details: Detail):
    cursor.execute('''INSERT INTO details ("Id", "Name", "Domain", "Age", "Email", "Is_student", "Rating") VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *;''',
                   (details.Id,details.Name, details.Domain, details.Age, details.Email, details.Is_student, details.Rating))
    insert_Detail = cursor.fetchone()
    conn.commit()
    return insert_Detail

# Deleting details
@app.delete("/details/{Id}")
def delete_post(Id: int):
    cursor.execute('DELETE FROM details WHERE "Id" = %s', (Id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Detail not found")
    return {"message": "Detail deleted successfully"}
    
# Updating details
@app.put("/details/{Id}")
def update_post(Id: int, details: Detail):
    cursor.execute('''UPDATE details SET "Name" = %s, "Domain" = %s, "Age" = %s, "Email" = %s, "Is_student" = %s, "Rating" = %s WHERE "Id" = %s RETURNING *;''',
                     (details.Name, details.Domain, details.Age, details.Email, details.Is_student, details.Rating, details.Id))
    updated_detail = cursor.fetchone()
    conn.commit()
    print(updated_detail)
    if not updated_detail:
        raise HTTPException(status_code=404, detail="Detail not found")
    return {"message": "Detail updated successfully"}