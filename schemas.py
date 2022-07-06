from typing import Optional
from pydantic import BaseModel
import strawberry

@strawberry.type
class Account:
    id: str
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]

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