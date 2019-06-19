

from .serializers import UserSerializer,UserUpdateSerializer,Mysite,UserUpdatev2Serializer

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
from rest_framework.permissions import IsAuthenticated

class UserViewSetView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        self.serializer_class=Mysite

        return self.retrieve(request, *args, **kwargs)
        # try:
        #     user = User.objects.get(id=self.argspk)
        # except User.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        #     # serializer = UserSerializer(user)
        # return Response({'id': user.pk, 'username': user.username}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # TODO 设置 permission_classes 开启


        print("1111",self.kwargs["pk"])
        print(request.data)
        # users/(?P<pk>\d+)/  self.kwargs["pk"] 得到URLpk
        user = request.user
        print(user.pk)
        if int(request.user.pk) ==int(self.kwargs["pk"]):


            # 获取到原来的信息
            # name = user.name
            # location = user.location

            serializer = UserUpdatev2Serializer(data=request.data)
            if serializer.is_valid():

                user.name=serializer.data['name']
                user.location=serializer.data['location']
                user.about_me=serializer.data['about_me']
                user.save()

                return Response({'status': 'ok', 'id': user.pk, 'username': user.username})

            else:
                print(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        # TODO 危险 需要判断
        print(request)
        if int(request.user.pk) == int(self.kwargs["pk"]):
            return self.destroy(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)




