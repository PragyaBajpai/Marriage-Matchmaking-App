from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas, json
from typing import List

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# function to convert the user model to the user schema to handle the intrests field
def convert_user_model(user_model: schemas.User) -> schemas.User:
    interests = (
        json.loads(user_model.interests)
        if isinstance(user_model.interests, str)
        else user_model.interests
    )
    return models.User(
        id=user_model.id,
        name=user_model.name,
        age=user_model.age,
        gender=user_model.gender,
        email=user_model.email,
        city=user_model.city,
        interests=interests,
    )


# create user api endpoint to create a new user ensuring that the email is unique
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    user_data = user.model_dump()
    user_data["interests"] = json.dumps(user_data["interests"])

    db_user = models.User(**user_data)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="An error occurred while saving the user."
        )

    db_user.interests = json.loads(db_user.interests)

    return db_user


# get user api to get all users
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return [convert_user_model(user) for user in users]


# get user api to get a specific user
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return convert_user_model(user)


# update user api to update a specific user
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "interests" and value is not None:
            value = json.dumps(value)
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    db_user.interests = json.loads(db_user.interests)
    return convert_user_model(db_user)


@app.delete("/users/{user_id}", response_model=schemas.Message)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:

        db_user = db.query(models.User).filter(models.User.id == user_id).first()

        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        db_user.interests = json.loads(db_user.interests)

        db.delete(db_user)
        db.commit()

        return schemas.Message(message="User deleted successfully")
    except HTTPException as http_exc:

        raise http_exc

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500, detail="An error occurred while deleting the user"
        )


@app.get("/users/{user_id}/matches", response_model=List[schemas.User])
def find_matches(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    requested_user_interests = (
        json.loads(user.interests)
        if isinstance(user.interests, str)
        else user.interests
    )
    requested_user_interests_set = set(requested_user_interests)
    all_users = (
        db.query(models.User)
        .filter(models.User.id != user_id, models.User.city == user.city)
        .all()
    )

    min_common_interests = 1
    matches = []
    for u in all_users:
        current_user_interests = (
            json.loads(u.interests) if isinstance(u.interests, str) else u.interests
        )
        current_user_interests_set = set(current_user_interests)
        common_interests = current_user_interests_set.intersection(
            requested_user_interests_set
        )
        if len(common_interests) >= min_common_interests:
            matches.append(convert_user_model(u))
    if not matches:
        raise HTTPException(status_code=404, detail="No matches found")
    return matches
