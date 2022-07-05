from pydantic import BaseModel
import strawberry

@strawberry.type
class Account:
    email: str
    first_name: str
    last_name: str
    password: str

@strawberry.input
class CreateAccountInput:
    email: str
    first_name: str
    last_name: str
    password: str

@strawberry.input
class CreateSessionsInput:
    email: str
    password: str