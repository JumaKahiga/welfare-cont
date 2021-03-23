from rest_framework import serializers

from members.models import Member


class MembersSerializer(serializers.HyperlinkedModelSerializer):
    my_dependants = serializers.StringRelatedField(many=True)
    contributions = serializers.StringRelatedField(many=True)
    total_contributions = serializers.ReadOnlyField()

    class Meta:
        model = Member
        fields = [
            'first_name', 'last_name', 'avatar', 'email',
            'phone_number', 'is_active', 'my_dependants',
            'contributions', 'total_contributions'
            ]


class MemberSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Member
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'paid_up']
