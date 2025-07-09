import graphene
from asgiref.sync import sync_to_async
from graphene import relay
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id

from .models import DeployedApp, Plan, User


PlanEnum = graphene.Enum.from_enum(Plan)


class CustomNode(relay.Node):
    TYPE_MAP = {}

    @staticmethod
    def from_global_id(global_id):
        if global_id.startswith('u_'):
            return ('User', global_id.replace('u_', ''))
        if global_id.startswith('app_'):
            return ('App', global_id.replace('app_', ''))
        return from_global_id(global_id)

    @classmethod
    def get_node_from_global_id(cls, info, global_id, only_type=None):
        type_name, obj_id = cls.from_global_id(global_id)

        if only_type:
            assert type_name == only_type._meta.name
            return only_type.get_node(info, obj_id)

        node_type = cls.TYPE_MAP.get(type_name)
        if node_type:
            return node_type.get_node(info, obj_id)

        return None


class UserNode(DjangoObjectType):
    id = graphene.ID(required=True)
    plan = PlanEnum()

    class Meta:
        model = User
        interfaces = (CustomNode,)
        name = 'User'

    def resolve_id(self, info):
        return f'u_{self.id}'

    @classmethod
    async def get_node(cls, info, id):
        try:
            return await User.objects.aget(id=id)
        except User.DoesNotExist:
            return None


class AppNode(DjangoObjectType):
    id = graphene.ID(required=True)

    class Meta:
        model = DeployedApp
        interfaces = (CustomNode,)
        name = 'App'

    def resolve_id(self, info):
        return f'app_{self.id}'

    @classmethod
    async def get_node(cls, info, id):
        try:
            return await DeployedApp.objects.select_related('owner').aget(id=id)
        except DeployedApp.DoesNotExist:
            return None


CustomNode.TYPE_MAP = {
    'User': UserNode,
    'App': AppNode,
}


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        plan = PlanEnum(required=False, default_value=Plan.HOBBY)

    user = graphene.Field(UserNode)

    async def mutate(root, info, username, plan):
        user = await User.objects.acreate(username=username, plan=plan)
        return CreateUser(user=user)


class CreateApp(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        active = graphene.Boolean(required=False, default_value=True)

    app = graphene.Field(AppNode)

    async def mutate(root, info, user_id, active):
        raw_id = user_id.replace('u_', '')
        user = await User.objects.filter(id=raw_id).afirst()
        if not user:
            raise Exception('User not found')

        app = await DeployedApp.objects.acreate(owner=user, active=active)
        return CreateApp(app=app)


class UpgradeAccount(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserNode)
    error = graphene.String()

    async def mutate(root, info, user_id):
        raw_id = user_id.replace('u_', '')
        user = await User.objects.filter(id=raw_id).afirst()

        if not user:
            return UpgradeAccount(ok=False, error='User not found', user=None)

        user.plan = Plan.PRO
        await user.asave()

        return UpgradeAccount(ok=True, user=user)


class DowngradeAccount(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserNode)
    error = graphene.String()

    async def mutate(root, info, user_id):
        raw_id = user_id.replace('u_', '')
        user = await User.objects.filter(id=raw_id).afirst()

        if not user:
            return DowngradeAccount(ok=False, error='User not found', user=None)

        user.plan = Plan.HOBBY
        await user.asave()

        return DowngradeAccount(ok=True, user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_app = CreateApp.Field()
    upgrade_account = UpgradeAccount.Field()
    downgrade_account = DowngradeAccount.Field()


class Query(graphene.ObjectType):
    node = CustomNode.Field()
    all_users = graphene.List(UserNode)
    all_apps = graphene.List(AppNode)

    async def resolve_all_users(root, info):
        return await sync_to_async(list)(User.objects.all())

    async def resolve_all_apps(root, info):
        queryset = DeployedApp.objects.select_related('owner')
        return await sync_to_async(list)(queryset)


schema = graphene.Schema(query=Query, mutation=Mutation, types=[UserNode, AppNode])
