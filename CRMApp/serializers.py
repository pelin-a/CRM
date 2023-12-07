from rest_framework import serializers
from .models import *
 

        
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields='__all__'
        extra_kwargs = {
            'notes': {'required': False},
        }
        def create(self, validated_data):
        # Access the logged-in user through the request context
            user = self.context['request'].user

        # Associate the logged-in user's ID with the model instance being created
            validated_data['user'] = user
            return super().create(validated_data)
        
class PipelineSerializer(serializers.ModelSerializer):
    # contact= ContactSerializer()
    # contact = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all())
    contact = serializers.SerializerMethodField()
    
    def get_contact(self, obj):
        if self.context.get('request').method in ['POST', 'PUT', 'PATCH']: 
            return obj.contact.id if obj.contact else None
        else:
            # For displaying data, return the serialized Contact data
            return ContactSerializer(obj.contact).data if obj.contact else None

    class Meta:
        model=Pipeline
        fields='__all__'
        extra_kwargs = {
            'due_date': {'required': False},
            'event': {'required': False},
            'notes': {'required': False},
        }
        
        def create(self, validated_data):
        # Access the logged-in user through the request context
            user = self.context['request'].user

        # Associate the logged-in user's ID with the model instance being created
            validated_data['user'] = user
            return super().create(validated_data)
      
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        return user