from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import AsyncGraphQLView

from .schema import schema

@csrf_exempt
async def graphql_view(request: HttpRequest):
    view = AsyncGraphQLView.as_view(graphiql=True, schema=schema)
    return await view(request)
