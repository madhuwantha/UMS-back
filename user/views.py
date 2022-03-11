from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User, Property, Notification
from user.serializers import UserSerializer
# from rest_framework.parsers import JSONParser
from django.forms.models import model_to_dict
from rest_framework.permissions import IsAuthenticated


def index(request):
    return render(request, 'index.html')


class UserPropertyAddView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        try:
            user_id = request.data["user_id"]
            radius = request.data["radius"]
            latitude = request.data["latitude"]
            longitude = request.data["longitude"]
            property_name = request.data["property_name"]
            property_address = request.data["property_address"]

            p = Property(
                radius=radius,
                latitude=latitude,
                longitude=longitude,
                property_name=property_name,
                property_address=property_address,
                user=User.objects.get(pk=user_id)
            )
            p.save()
            return Response({'status': True})
        except Exception as e:
            print(e.with_traceback())
            return Response({'error': e.__str__()})


class UserAddView(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = [JSONParser]

    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user_name = request.data["user_name"]
            email = request.data["email"]
            device_token = request.data["device_token"]
            is_premium_user = request.data["is_premium_user"]
            did_accept_to_sand_privacy_policy = request.data["did_accept_to_sand_privacy_policy"]
            date_accepted_to_sand_privacy_policy = request.data["date_accepted_to_sand_privacy_policy"]
            fire_monitoring_is_on = request.data["fire_monitoring_is_on"]
            weather_monitoring_is_on = request.data["weather_monitoring_is_on"]

            u = User(
                user_name=user_name,
                email=email,
                device_token=device_token,
                is_premium_user=is_premium_user,
                did_accept_to_sand_privacy_policy=did_accept_to_sand_privacy_policy,
                date_accepted_to_sand_privacy_policy=date_accepted_to_sand_privacy_policy,
                fire_monitoring_is_on=fire_monitoring_is_on,
                weather_monitoring_is_on=weather_monitoring_is_on
            )
            u.save()
            properties = list(request.data["properties"])
            for property in properties:
                radius = property["radius"]
                latitude = property["latitude"]
                longitude = property["longitude"]
                property_name = property["property_name"]
                property_address = property["property_address"]
                p = Property(
                    radius=radius,
                    latitude=latitude,
                    longitude=longitude,
                    property_name=property_name,
                    property_address=property_address,
                    user=u
                )
                p.save()
            return Response({'status': True})
        except Exception as e:
            print(e.with_traceback())
            return Response({'error': e.__str__()})


class UserView(APIView):
    """This endpoint list all the available Users from the database"""

    def get(self, request, id):
        u = User.objects.get(pk=id)
        u = model_to_dict(u)
        p = list(Property.objects.filter(user=id).values())
        u['properties'] = p
        return JsonResponse(u)


class ListUserAPIView(ListAPIView):
    """This endpoint allows for creation of a User"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUserAPIView(CreateAPIView):
    """This endpoint allows for creation of a User"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UpdateUserAPIView(UpdateAPIView):
    """This endpoint allows for updating a specific User by passing in the id of the User to update"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DeleteUserAPIView(DestroyAPIView):
    """This endpoint allows for deletion of a specific User from the database"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
