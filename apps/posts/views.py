from rest_framework import viewsets
from .serializers import PostSerializer
from .models import Post
from apps.api.permissions import IsAccountAdminOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAccountAdminOrReadOnly]
