from rest_framework import serializers

from funds.models import Contribution, Disbursement


class FundsSerializer(serializers.ModelSerializer):
    lifetime_contributions = serializers.SerializerMethodField()
    available_funds = serializers.SerializerMethodField()
    monthly_contributions = serializers.SerializerMethodField()
    annual_contributions = serializers.SerializerMethodField()

    def get_lifetime_contributions(self, instance):
        return instance.total_contribution()

    def get_available_funds(self, instance):
        return instance.available_funds()

    def get_monthly_contributions(self, instance):
        return instance.total_monthly_contributions()

    def get_annual_contributions(self, instance):
        return instance.total_annual_contributions()

    class Meta:
        model = Contribution

        fields = [
            'current_period',
            'lifetime_contributions', 'available_funds',
            'monthly_contributions', 'annual_contributions'
        ]


class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution

        fields = ['member', 'month', 'year', 'amount', 'payment_date']
