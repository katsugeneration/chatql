# coding=utf-8
#
# Licensed under the MIT License
"""GraphQL accessor."""
import graphene


class Query(graphene.ObjectType):
    """Query Type."""

    hello = graphene.String(description='A typical hello world')

    def resolve_hello(self, info):
        """Hello param."""
        return 'World'


schema = graphene.Schema(query=Query)
