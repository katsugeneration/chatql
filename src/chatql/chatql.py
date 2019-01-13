# coding=utf-8
#
# Licensed under the MIT License
"""GraphQL scheme define."""
import graphene
import json


class User(graphene.ObjectType):
    """User Type."""

    id = graphene.ID()
    optional_args = graphene.String()

    def resolve_optional_args(self, info):
        """User optional parameters resolver."""
        engine = info.context['engine']
        attributes = engine.get_user_attributes(self.id)
        return json.dumps(attributes)


class Response(graphene.ObjectType):
    """System Response Type."""

    id = graphene.ID()
    user = graphene.Field(User)
    request = graphene.String(description='User input request')
    text = graphene.String(description='System response string')


class Query(graphene.ObjectType):
    """Query Type."""

    response = graphene.Field(
                    Response,
                    request=graphene.String(required=True),
                    user=graphene.ID())
    user = graphene.Field(User, id=graphene.ID(required=True))

    def resolve_response(self, info, request=None, user=None):
        """Request param resolver."""
        engine = info.context['engine']
        res_history = engine.generate_response_text(
            request,
            user=user)
        return Response(
            id=res_history.id,
            request=request,
            user=User(id=res_history.user.id),
            text=res_history.scenario['response'])

    def resolve_user(self, info, id=None):
        """User param resolver."""
        return User(id=id)


class CreateUser(graphene.Mutation):
    """Crete User Mutation."""

    class Arguments:
        """Mutation Arguments."""

        optional_args = graphene.String()

    user = graphene.Field(lambda: User)

    def mutate(self, info, optional_args=None):
        """Mutate function."""
        engine = info.context['engine']
        if optional_args is None:
            id = engine.create_new_user()
        else:
            id = engine.create_new_user(**json.loads(optional_args))
        user = User(id=id, optional_args=optional_args)
        return CreateUser(user=user)


class Mutations(graphene.ObjectType):
    """Chatql Schema Mutations."""

    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
