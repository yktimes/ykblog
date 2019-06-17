

from .serializers import UserSerializer,UserUpdateSerializer

from . models import User

from rest_framework  import status
from rest_framework.views import APIView

from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin
)
from rest_framework.generics import GenericAPIView

from rest_framework.response import Response


class UserViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):

    # queryset和serializer_class是固定写法
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            user = serializer.save()

            # '_links': {
            #     'self': reverse("user-retrieve", id=self.id)
            # }
            #
            return Response({'status': 'ok', 'id': user.pk, 'username': user.username})

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        # return self.create(request, *args, **kwargs)

class UserViewSetView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer



    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
        # try:
        #     user = User.objects.get(id=self.argspk)
        # except User.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        #     # serializer = UserSerializer(user)
        # return Response({'id': user.pk, 'username': user.username}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # TODO 设置 permission_classes 开启
        # if request.user.pk!=self.kwargs["pk"]:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            print("1111",self.kwargs["pk"])
            print(request.data)
            # users/(?P<pk>\d+)/  self.kwargs["pk"] 得到URLpk
            user = User.objects.get(id=self.kwargs["pk"])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            # 获取到原来的信息
            email = user.email
            username = user.username

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():

                user.email=serializer.data.get("email") if serializer.data.get("email") else email
                user.username=serializer.data.get("username") if serializer.data.get("username") else username
                user.save()

                return Response({'status': 'ok', 'id': user.pk, 'username': user.username})

            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # TODO 危险 需要判断
        return self.destroy(request, *args, **kwargs)





class TokenView(APIView):

    def post(self,request):
        print(request.data)

        return Response({"aa":11})