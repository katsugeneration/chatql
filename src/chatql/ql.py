# coding=utf-8
#
# Licensed under the MIT License
"""GraphQL accessor."""
import graphene


class Response(graphene.ObjectType):
    id = graphene.ID()
    text = graphene.String(description='system response string')

    def resolve_text(self, info):
        return 'hello!'


class Query(graphene.ObjectType):
    """Query Type."""
    response = graphene.Field(Response)

    def resolve_response(self, info):
        """Hello param."""
        return Response()


schema = graphene.Schema(query=Query)
