# scholar-match/serializers.py

from rest_framework import serializers
from .models import ScholarMatch

class ScholarMatchSerializer(serializers.ModelSerializer):
  class Meta:
    model = ScholarMatch
    fields = ('id', 'title', 'description', 'completed')
