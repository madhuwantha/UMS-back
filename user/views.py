from datetime import timedelta, datetime
import time
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
from user.notification import save_notification, send_notification, sent_fire_notification
from user.serializers import UserSerializer
# from rest_framework.parsers import JSONParser
from django.forms.models import model_to_dict
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from user.utils import fire_api, get_tim_in_zone


def index(request):
    return render(request, 'index.html')


class Test(APIView):

    def post(self, request):

        sent_fire_notification()
        d = int(time.time())
        dt = get_tim_in_zone(d)
        h = dt.hour
        if h > 8:
            d = dt.day
            dt = dt.replace(hour=8, minute=0, second=0, day=d + 1)
        else:
            dt = dt.replace(hour=8, minute=0, second=0)

        print(d)


class UserPropertyRemoveView(APIView):
    parser_classes = [JSONParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            p_id = request.data["p_id"]
            u = Property.objects.get(pk=p_id).delete()
            return JsonResponse({"status": True})
        except Exception as e:
            print(e.__str__())
            return Response({'error': e.__str__()})


class UserPropertyAddView(APIView):
    parser_classes = [JSONParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user_id = request.data["user_id"]
            u = User.objects.get(custom_id=user_id)
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
                user=u
            )
            p.save()
            return Response({'status': True})
        except Exception as e:
            print(e.__str__())
            return Response({'error': e.__str__()})


class UserAddView(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = [JSONParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user_id = request.data["user_id"]
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
                weather_monitoring_is_on=weather_monitoring_is_on,
                custom_id=user_id
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
            print(e.__str__())
            return Response({'error': e.__str__()})


class UserView(APIView):
    """This endpoint list all the available Users from the database"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            u = User.objects.filter(custom_id=id)[0]
            u = model_to_dict(u)
            p = list(Property.objects.filter(user=u["id"]).values())
            u['properties'] = p
            return JsonResponse(u)
        except Exception as e:
            print(e.__str__())
            return Response({'error': e.__str__()})


class ListUserAPIView(ListAPIView):
    """This endpoint allows for creation of a User"""
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUserAPIView(CreateAPIView):
    """This endpoint allows for creation of a User"""
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UpdateUserAPIView(UpdateAPIView):
    """This endpoint allows for updating a specific User by passing in the id of the User to update"""
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDeleteAPIView(APIView):
    """This endpoint allows for deletion of a specific User from the database"""
    parser_classes = [JSONParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        u = User.objects.filter(custom_id=request.data["custom_id"]).delete()
        return JsonResponse({"status": True})
