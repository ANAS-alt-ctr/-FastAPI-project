from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr,Field
import json
from fastapi import Query

app = FastAPI()

with open("users.json", "r") as a:
    users = json.load(a)

@app.get("/")
def get_users():
    global users
    return users

class UserCreate(BaseModel):
    name: str
    age: int
    city: str
    email: EmailStr
    review: str=Field(min_length=1,max_length=200)

@app.get("/users{parameters}")
def get_users(
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0),
    sort: str = Query("asc")
):

    if limit <= 0:
        raise HTTPException(status_code=400, detail="limit must be positive")

    if offset < 0:
        raise HTTPException(status_code=400, detail="offset must be zero or positive")

    sort = sort.lower()

    if sort not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="sort must be asc or desc")

    reverse = sort == "desc"

    users_sorted = sorted(users, key=lambda x: x["id"], reverse=reverse)

    return users_sorted[offset: offset + limit]

@app.post("/users")
def create_user(user: UserCreate):
    if not user.review or not user.review.strip():
        raise HTTPException(status_code=400, detail="Review cannot be empty")
    
    if len(user.review) > 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Review cannot exceed 200 characters")

    analysis = {
        "word_count": len(user.review.split()),
        "uppercase_letters": sum(1 for letter in user.review if letter.isupper()),
        "special_characters": sum(1 for c in user.review if not c.isalnum() and not c.isspace())
    }

    user_data = {
        "id": len(users) + 1,
        "name": user.name,
        "age": user.age,
        "city": user.city,
        "email": user.email,
        "review": user.review,
        "analysis": analysis
    }
    users.append(user_data)
    with open("users.json", "w") as b:
        json.dump(users, b, indent=4) 
    return user_data

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            with open("users.json", "w") as b:
                json.dump(users, b) 
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.get("/Analyze/{user_id}")
def analyze_users(user_id: int):
    for user in users:
        if user["id"] == user_id:
            if "analysis" not in user:
                review_text = user["review"]
                user["analysis"] = {
                    "word_count": len(review_text.split()),
                    "uppercase_letters": sum(1 for letter in review_text if letter.isupper()),
                    "special_characters": sum(1 for c in review_text if not c.isalnum() and not c.isspace())
                }
    return {
                "user_id": user_id,
                **user["analysis"],
                "analyze_UUID": len(users) + 1
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.get("/users/{user_id}/analyses")
def get_analyses(
    user_id: int,
    limit: int = Query(5),
    offset: int = Query(0),
    sort: str = Query("asc"),
    min_words: int = Query(None)
):
    if limit <= 0:
        raise HTTPException(status_code=400, detail="limit must be positive")

    if offset < 0:
        raise HTTPException(status_code=400, detail="offset must be zero or positive")

    if sort not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="sort must be 'asc' or 'desc'")

    if min_words is not None and min_words < 0:
        raise HTTPException(status_code=400, detail="min_words must be positive")

    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    analyses = list(user.get("analyses", {}).values())

    if min_words is not None:
        analyses = [a for a in analyses if a["word_count"] >= min_words]

    reverse = True if sort == "desc" else False
    analyses = sorted(analyses, key=lambda x: x["analysis_id"], reverse=reverse)    
    result = analyses[offset: offset + limit]

    return result