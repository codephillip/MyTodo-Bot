import json, requests, random, re

from django.utils.crypto import get_random_string
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

PAGE_ACCESS_TOKEN = "EAACDVIAXlXoBACdKWbRLaq1rcJi9ON4MNzSjFnAY82ZAew3WNkHnxS79lVCyFGj1CI8SdtL50wMezcGYi5zSdhhCIjgvn85FgkqnocJn6P2uIpNLZAX7iiceHfdQdBe6JRq8ZAGy5sDSlm4ZCqnHTWb0ua266RUeYsUpn97JIhWLhLZABEYDd"
VERIFY_TOKEN = "12341234"


def post_facebook_message(fbid, received_message):
    user_details_url = "https://graph.facebook.com/v2.6/%s" % fbid
    user_details_params = {'fields': 'first_name,last_name,profile_pic', 'access_token': PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()

    random_text = get_random_string(length=30)
    random_text = 'Yo ' + user_details['first_name'] + ' Did you say ' + received_message + '. This is what I think ' + random_text

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": random_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(status.json())


class MyTodoBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET.get('hub.verify_token') == VERIFY_TOKEN:
            return HttpResponse(self.request.GET.get('hub.challenge'))
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    print(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()
