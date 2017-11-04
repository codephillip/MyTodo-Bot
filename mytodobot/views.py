import json, requests

from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from mytodobot.models import Task

PAGE_ACCESS_TOKEN = "EAACDVIAXlXoBACdKWbRLaq1rcJi9ON4MNzSjFnAY82ZAew3WNkHnxS79lVCyFGj1CI8SdtL50wMezcGYi5zSdhhCIjgvn85FgkqnocJn6P2uIpNLZAX7iiceHfdQdBe6JRq8ZAGy5sDSlm4ZCqnHTWb0ua266RUeYsUpn97JIhWLhLZABEYDd"
VERIFY_TOKEN = "12341234"


def post_facebook_message(fbid, reply):
    user_details_url = "https://graph.facebook.com/v2.6/%s" % fbid
    user_details_params = {'fields': 'first_name,last_name,profile_pic', 'access_token': PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()

    reply = 'Hi ' + user_details['first_name'] + ' ' + reply
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": reply}})
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
                    reply = self.process_message(message, message['recipient']['id'])
                    post_facebook_message(message['sender']['id'], reply)
        return HttpResponse()

    def process_message(self, message, receiver_id):
        message_text = message['message']['text']
        if '/add' in message_text:
            reply = 'Successfully added task'
            refined_message_text = message_text.replace('/add ', '')
            Task(userid=receiver_id, text=refined_message_text).save()
        elif '/edit' in message_text:
            reply = 'Successfully edited task'
            message_id = message_text[4:7]
            print("MESSAGE ID")
            print(message_id)
            # Task.objects.get(id=message_id)
        elif '/delete' in message_text:
            reply = 'Successfully deleted task'
        elif '/show' in message_text:
            reply = 'show'
        else:
            reply = '\nWelcome to Mytodo bot.\nPlease use the commands below.\n  ' \
                    'ALL TASKS: /show \n  ADD TASK: /add <Message> \n  DELETE TASK: /delete <Task No> \n  ' \
                    'EDIT TASK: /edit <Task No> <Message>'
        return reply
