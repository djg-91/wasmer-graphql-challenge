from django.http import HttpRequest
from graphene_django.views import AsyncGraphQLView

from .schema import schema


async def graphql_view(request: HttpRequest):
    view = AsyncGraphQLView.as_view(graphiql=True, schema=schema)
    return await view(request)
