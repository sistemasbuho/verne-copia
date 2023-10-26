from rest_framework import serializers
from ..models import Meeting,UserVotes

class MeetingSerializer(serializers.ModelSerializer):
	# id_idea = serializers.StringRelatedField(read_only=True, many=True)

	class Meta:
		model = Meeting
		fields = 'id','name',"date","place","start_time","end_time","is_active","id_idea"


class UserVotesSerializer(serializers.ModelSerializer):
	id_idea = serializers.StringRelatedField(read_only=True)
	id_user_comitte=serializers.StringRelatedField(read_only=True)
	id_meeting=serializers.StringRelatedField(read_only=True)

	class Meta:
		model = UserVotes
		fields ="id","vote","id_meeting","id_idea","id_user_comitte","is_evaluate","phase_actual","message","pub_date"