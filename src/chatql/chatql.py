# coding=utf-8
#
# Licensed under the MIT License
"""GraphQL schame define."""
import graphene


class Response(graphene.ObjectType):
    """System Response Type."""

    id = graphene.ID()
    request = graphene.String(description='User input request')
    text = graphene.String(description='System response string')

    def resolve_text(self, info):
        """Text param resolver."""
        data_accessor = info.context['data_accessor']
        return data_accessor.get_response_text(self.request)


class Query(graphene.ObjectType):
    """Query Type."""

    response = graphene.Field(Response, request=graphene.String(required=True))

    def resolve_response(self, info, request=None):
        """Request param resolver."""
        return Response(request=request)


schema = graphene.Schema(query=Query)
