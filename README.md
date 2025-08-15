# FastAPI Chat Project

This is a minimal FastAPI project with a single POST `/chat` endpoint, following standard folder structure practices.

## Project Structure

```
app/
  main.py
  api/
    chat.py
  models/
    chat.py
requirements.txt
```

## How to Run

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Start the server:
   ```sh
   uvicorn app.main:app --reload
   ```
3. The POST `/chat` endpoint will be available at `http://localhost:8000/chat`.

## Example Request

```
POST /chat
{
  "message": "Hello!"
}
```

Response:

```
{
  "reply": "Echo: Hello!"
}
```
