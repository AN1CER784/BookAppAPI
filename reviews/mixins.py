from rest_framework import viewsets


class UserSerializerMixin:
    def perform_create(self: viewsets.ModelViewSet, serializer):
        serializer.save(user=self.request.user)