from rest_framework import serializers
from payment_system.models import (
    Project,
    ProjectSubscription,
    UserProject,
    Subscription,
    Invoice,
    Invitation,
)


class ProjectSubscriptionSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return ProjectSubscription.create(**validated_data)

    class Meta:
        model = ProjectSubscription
        read_only_fields = ['status', 'expiring_date']
        fields = [
            'id', 'project', 'subscription'
        ] + read_only_fields


class SubscriptionToProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='subscription.id')
    name = serializers.CharField(source='subscription.name')
    price = serializers.IntegerField(source='subscription.price')
    requests_limit = serializers.IntegerField(source='subscription.requests_limit')
    duration = serializers.IntegerField(source='subscription.duration')
    grace_period = serializers.IntegerField(source='subscription.duration')

    class Meta:
        model = ProjectSubscription
        fields = [
            'id', 'name', 'status', 'expiring_date',
            'price', 'requests_limit', 'duration', 'grace_period',
        ]
        read_only_fields = fields


class UserInProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    name = serializers.CharField(source='user.get_full_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProject
        fields = [
            'id', 'name', 'email', 'status', 'role', 'is_default',
        ]
        read_only_fields = fields


class ProjectListSerializer(serializers.ModelSerializer):
    is_default = serializers.SerializerMethodField(read_only=True)
    role = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    owner = serializers.CharField(source='owner.get_full_name', read_only=True)

    def get_is_default(self, obj):
        return obj.user_projects.get(user=self.context['request'].user).is_default

    def get_role(self, obj):
        return obj.user_projects.get(user=self.context['request'].user).role

    def get_status(self, obj):
        return obj.user_projects.get(user=self.context['request'].user).status

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'is_active',
            'is_default', 'role', 'status', 'owner',
        ]
        read_only_fields = fields


class ProjectInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'email', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    subscriptions = SubscriptionToProjectSerializer(source='project_subscriptions',
                                                    many=True, read_only=True)
    users = UserInProjectSerializer(source='user_projects',
                                    many=True, read_only=True)
    is_default = serializers.SerializerMethodField(read_only=True)
    invitations = ProjectInvitationSerializer(many=True, read_only=True)

    owner = serializers.CharField(source='owner.get_full_name', read_only=True)
    is_owner = serializers.SerializerMethodField(read_only=True)

    def get_is_owner(self, obj):
        return obj.user_projects.get(user=self.context['request'].user).role == UserProject.OWNER

    def get_is_default(self, obj):
        return obj.user_projects.get(user=self.context['request'].user).is_default

    def create(self, validated_data):
        user = self.context['request'].user
        return Project.create(
            owner=user,
            name=validated_data['name'],
            description=validated_data.get('description', ''),
        )

    class Meta:
        model = Project
        read_only_fields = [
            'users', 'subscriptions', 'invitations', 'token',
            'is_active', 'is_default', 'disabled_at', 'owner',
            'created_at', 'is_owner',
        ]
        fields = [
            'id', 'name', 'description',
        ] + read_only_fields


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        read_only_fields = (
            'id', 'custom', 'name', 'description', 'price',
            'requests_limit', 'duration', 'grace_period',
        )
        fields = read_only_fields


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        read_only_fields = (
            'id', 'paid_at', 'info', 'project', 'subscription',
        )
        fields = read_only_fields


class ProjectInviteUserSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']


class InvitationListSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(source='project.id', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    project_owner = serializers.CharField(source='project.owner.get_full_name', read_only=True)

    class Meta:
        model = Invitation
        fields = ['id', 'project_id', 'project_name', 'project_owner', 'updated_at']
        read_only_fields = fields
