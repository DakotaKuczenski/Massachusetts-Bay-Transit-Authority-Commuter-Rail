from django.shortcuts import render
from django.http import HttpResponse, response, JsonResponse
import requests
from requests.api import request
from django.conf import settings
import logging

# logger = logging.getLogger(__name__)                                                  # *logger is not configured*


def disection(dataList, objectID):
    for x in dataList:
        if x.get("id") == objectID:
            return x
    return None


def apiResponseFormat(data):
    info = data.get("included")
    departureInfo = data.get("data")
    responseData = {}
    responseData["departure"] = []
    parseDepart = []
    allTrips = []
    allStops = []
    allSchedules = []
    allRoute = []

    for i in info:
        if i["type"] == "trip":
            allTrips.append(i)
        elif i["type"] == "schedule":
            allSchedules.append(i)
        elif i["type"] == "stop":
            allStops.append(i)

    for ride in departureInfo:
        if (
            ride.get("attributes")["departure_time"]
            and not ride.get("attributes")["arrival_time"]
        ):
            parseDepart.append(ride)

    if parseDepart:
        for ride in parseDepart:

            returned = {}

            status = ride.get("attributes")["status"]
            destination = ride.get("relationships")["route"]["data"]["id"]
            stopID = ride.get("relationships")["stop"]["data"]["id"]

            stopInfo = disection(allStops, stopID)

            trainTrack = stopInfo.get("attributes")["platform_code"]
            tripID = ride.get("relationships")["trip"]["data"]["id"]
            tripInfo = disection(allTrips, tripID)
            vehicle = tripInfo.get("attributes")["name"]
            scheduleID = ride.get("relationships")["schedule"]["data"]["id"]
            scheduleInfo = disection(allSchedules, scheduleID)
            departureTime = scheduleInfo.get("attributes")["departure_time"]

            name = destination[3:]

            if trainTrack is None:
                trainTrack = "None"

            returned = {
                "route_ID": destination,
                "destination": name,
                "next departure": departureTime,
                "status": status,
                "Train Number": vehicle,
                "track number": trainTrack,
            }
            responseData["departure"].append(returned)

    return responseData


def commuterRail(request):
    # only north station

    url = "https://api-v3.mbta.com/predictions?filter[stop]=place-north&filter[route_type]=2&include=stop,trip,schedule"
    response = requests.get(url)
    data = response.json()
    data = apiResponseFormat(data)

    x = []
    for i in range(0, len(data["departure"])):
        x.append(data["departure"][i])

    return render(request, "commuterRail.html", {"res": x})


def home(request):
    return render(request, "home.html")
