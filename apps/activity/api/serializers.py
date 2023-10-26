from rest_framework import serializers
from ..models import *


class ActivitySerializer(serializers.ModelSerializer):
	#id_idea = serializers.StringRelatedField(read_only=True, many=True)
	id_user =serializers.StringRelatedField(read_only=True,many=True)

	class Meta:
		model = Activity
		fields = "id","tool","description","name","date","score","redeemed_score","id_user","id_idea"





