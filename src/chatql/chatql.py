# coding=utf-8
#
# Licensed under the MIT License
"""GraphQL scheme define."""
import graphene


class User(graphene.ObjectType):
    """User Type."""

    id = graphene.ID()


class Response(graphene.ObjectType):
    """System Response Type."""

    id = graphene.ID()
    user = graphene.Field(User)
    request = graphene.String(description='User input request')
    text = graphene.String(description='System response string')

    def resolve_text(self, info):
        """Text param resolver."""
        engine = info.context['engine']
        return engine.generate_response_text(
            self.request,
            user_id=self.user.id)


class Query(graphene.ObjectType):
    """Query Type."""

    response = graphene.Field(
                    Response,
                    request=graphene.String(required=True),
                    user=graphene.ID())
    user = graphene.Field(User, id=graphene.ID(required=True))

    def resolve_response(self, info, request=None, user=None):
        """Request param resolver."""
        return Response(request=request, user=User(id=user))

    def resolve_user(self, info, id=None):
        """User param resolver."""
        return User(id=id)


class CreateUser(graphene.Mutation):
    """Crete User Mutation."""

    user = graphene.Field(lambda: User)

    def mutate(self, info):
        """Mutate function."""
        engine = info.context['engine']
        id = engine.create_new_user()
        user = User(id=id)
        return CreateUser(user=user)


class Mutations(graphene.ObjectType):
    """Chatql Schema Mutations."""

    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
