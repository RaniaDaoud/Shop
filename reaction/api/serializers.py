from rest_framework.serializers import ModelSerializer


from reaction.models import Reaction




#type = (('NORMAL', 'normal'), ('SMILE', 'smile'), ('LOVE', 'love'), ('WISH', 'wish'))
class ReactionCreateSerializer(ModelSerializer):
    
    def get_type(self, obj):
        
        return getattr(obj,'type', 'normal')

    class Meta:
        model = Reaction
        fields = ['type']
    
    

   