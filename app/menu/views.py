from datetime import date
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Restaurant, Vote, Menu

from menu import serializers


class BaseMenuAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base viewset for user owned menu attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(manu__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class RestaurantViewSet(BaseMenuAttrViewSet):
    """Manage Restaurant in the database"""
    queryset = Restaurant.objects.all()
    serializer_class = serializers.Restaurant


class VoteViewSet(viewsets.ModelViewSet):
    """Manage Vote in the database"""
    serializer_class = serializers.VoteSerializer
    queryset = Vote.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        winner = self.request.query_params.get('winner')
        queryset = self.queryset
        if winner:
            queryset = queryset.filter(winner=True)

        return queryset

    def perform_create(self, serializer):
        """Create a new vote"""
        user_id = self.request.user.id
        if not Vote.objects.filter(user_id=user_id, date=date.today).exists():
            serializer.save()


class MenuViewSet(viewsets.ModelViewSet):
    """Manage Menu in the database"""
    serializer_class = serializers.MenuSerializer
    queryset = Menu.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the Menu for the authenticated user"""
        winner = self.request.query_params.get('winner')
        queryset = self.queryset
        if winner:
            queryset = queryset.filter(winner=True)

        return queryset

    def perform_create(self, serializer):
        """Create a new menu"""
        serializer.save()
