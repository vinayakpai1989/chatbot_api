from .pushover import push

def record_user_details(email, name="unknown", notes="unknown"):
    push(f"New user details recorded: Email: {email}, Name: {name}, Notes: {notes}")
    return {"recorded": "OK"}

def record_unknown_question(question):
    push(f"New unknown question recorded: {question}")
    return {"recorded": "OK"}
