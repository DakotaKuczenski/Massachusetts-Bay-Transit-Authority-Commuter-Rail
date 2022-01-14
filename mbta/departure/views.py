from django.shortcuts import render
from django.http import HttpResponse, response, JsonResponse
import requests
from requests.api import request
import json
from functools import wraps
import logging 


# logger = logging.getLogger(__name__)                                                  # logger is not configured*

                                                             
def commuterRail(request): 

    if request.method != "GET":
        message = 'request is invalid'                                                  # log this when going into prod
        explanation = 'Server could not accept request, "GET" request required'
        return JsonResponse({'message': message, 'explanation' : explanation})

    try:  
        response = requests.get('https://api-v3.mbta.com/routes?filter[type]=2')

        if response.status_code != 200: 
            # logger.error("Not 200, error.")
            message = 'request is invalid'                                              # log this when going into prod, would also check for other status codes like 400/500
            explanation = 'Server could not accept request, returned bad status'        # to tell if error occured client or server side. <=400 & <=500
            return JsonResponse({'message': message, 'explanation' : explanation})

        json_list = []
        x = json.loads(response.text)
        for i in range(0, len(x['data'])):
            json_list.append(x['data'][i]['attributes'])
        return render(request, 'commuterRail.html',{'res': json_list})
    except Exception as error:
        error = 'Something went wrong'
        print('Caught error: ' + repr(error))
        


def home(request):
    return render(request, 'home.html')



