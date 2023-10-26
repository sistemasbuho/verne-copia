from rest_framework import serializers
from ..models import AssignedPrize,Action,UserLeguas

class PrizeSerializer(serializers.ModelSerializer):
	id_prize = serializers.StringRelatedField(read_only=True)
	id_user =serializers.StringRelatedField(read_only=True,many=True)

	class Meta:
		model = AssignedPrize
		fields = "id","date","id_user","id_prize"

class ActionSerializer(serializers.ModelSerializer):
	id_idea = serializers.StringRelatedField(read_only=True)
	id_activity =serializers.StringRelatedField(read_only=True)
	id_user =serializers.StringRelatedField(read_only=True,many=True)

	class Meta:
		model = Action
		fields = "id","date","name","description","score","id_idea","id_activity","id_user"


class LeguasSerializer(serializers.ModelSerializer):
	id_user =serializers.StringRelatedField(read_only=True)

	class Meta:
		model = UserLeguas
		fields = "id","quantity","category","id_user"


