from rest_framework import viewsets
from rest_framework.serializers import ModelSerializer


class UserSerializerMixin:
    def perform_create(self: viewsets.ModelViewSet, serializer: ModelSerializer):
        serializer.save(user=self.request.user)