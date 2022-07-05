from xmlrpc.client import Boolean
from fastapi import Depends, FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from database import db_session
from datetime import timedelta
import models
from strawberry.types import Info
from modules.auth.resolvers import IsAuthenticated, authenticate_user, create_access_token, current_user, get_password_hash
from schemas import Account, CreateAccountInput, CreateSessionsInput


db = db_session.session_factory()

app = FastAPI()

@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def me(self, info: Info) -> Account:
        user = await current_user(info)
        return user


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_account(self, input: CreateAccountInput ) -> Boolean: 
        account = Account(email=input.email, first_name=input.first_name, last_name=input.last_name, password=input.password)

        hash_password = get_password_hash(input.password) 

        db_account = models.AccountTable(email=account.email, first_name=account.first_name, last_name=account.last_name, hash_password=hash_password)
        db.add(db_account)
        db.commit()
        return True

    @strawberry.mutation
    def create_session(self, input: CreateSessionsInput) -> str:
        user = authenticate_user(input.email, input.password)
        if not user:
            raise Exception("Invalid username or password")
        token_expires = timedelta(minutes=60)
        token = create_access_token(user.email, user.id, expires_delta=token_expires)
        return token


def custom_context_dependency() -> str:
    return "John"        

async def get_context(custom_value=Depends(custom_context_dependency)):
    return {
        "custom_value": custom_value,
    }


schemas = strawberry.Schema(Query, Mutation)
graphql_app = GraphQLRouter(schemas, context_getter=get_context)


app.include_router(graphql_app, prefix="/graphql")