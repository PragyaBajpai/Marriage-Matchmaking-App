# Marriage Matchmaking App

## Brief Description
The Marriage Matchmaking App is a simple backend application designed to help users find potential matches based on their profile information. The app allows users to create, read, update, and delete profiles with details such as name, age, gender, email, city, and interests.

## Features

- **Create User**: Add a new user to the database.
- **Read Users**: Retrieve a list of users or a single user by ID.
- **Update User**: Modify user details.
- **Delete User**: Remove a user from the database.
- **Find Matches**: Find users with common interests and the same city.

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite (or other supported database)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repository.git
    cd your-repository
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the server**:
    ```bash
    uvicorn main:app --reload
    ```

2. **API Endpoints**:

    - **POST** `/users/` - Create a new user.
    - **GET** `/users/` - Retrieve a list of users.
    - **GET** `/users/{user_id}` - Retrieve a user by ID.
    - **PUT** `/users/{user_id}` - Update user details.
    - **DELETE** `/users/{user_id}` - Delete a user.
    - **GET** `/users/{user_id}/matches` - Find users with common interests.

## Example

### Create User

**Request:**

```http
POST /users/
Content-Type: application/json

{
    "name": "John Doe",
    "age": 30,
    "gender": "male",
    "email": "john.doe@example.com",
    "city": "New York",
    "interests": ["reading", "coding"]
}```

**Response:**
{
    "id": 1,
    "name": "John Doe",
    "age": 30,
    "gender": "male",
    "email": "john.doe@example.com",
    "city": "New York",
    "interests": ["reading", "coding"]
}

Postman API Collection- 
https://api.postman.com/collections/29977454-4c8a0a88-4e51-47e9-b888-7925cec72199?access_key=PMAT-01J4SA61AAW4EZD38S9RMPSJPD
