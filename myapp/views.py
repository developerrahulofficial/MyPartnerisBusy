import os

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from twilio.rest import Client
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from .models import CallStatus
from .models import Visitor


@csrf_exempt
def twilio_webhook(request):
    print("Webhook received")
    call_status = request.POST.get('CallStatus')
    if call_status is not None:
        call_id = request.POST.get('CallSid')  # Replace with the actual call ID field name
        CallStatus.objects.create(call_id=call_id, status=call_status)
    else:
        print("Nothing to show")
    return HttpResponse(status=200)

def index(request):
    visitor_count = Visitor.objects.count()
    return render(request, 'index.html', {'visitor_count': visitor_count})


@csrf_exempt
def make_call(request):
    if request.method == 'POST':
        # Retrieve the phone number from the POST data
        phone = request.POST.get('phone')

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        call = client.calls.create(
            url='http://demo.twilio.com/docs/voice.xml',
            to=phone,
            from_=settings.TWILIO_PHONE_NUMBER,
            record=True,
            status_callback='https://7264-103-212-158-183.ngrok-free.app/twilio_webhook/',
            status_callback_event=['completed', 'busy', 'no-answer', 'failed', 'canceled'],
            status_callback_method='POST'
        )

        # Access the call ID (SID) from the call object
        call_id = call.sid
        print("This is call id :",call_id)
        # Set the callId as a session variable
        request.session['callId'] = call_id

        # Save the session
        request.session.save()

        return JsonResponse({"status": call.status, "call_id": call_id})
    else:
        # Handle the case where the request method is not POST
        return JsonResponse({"error": "Invalid request method"})

@csrf_exempt
def check_call_status(request):
    call_id = request.session.get('callId')
    print("this is call id in check_call_status :",call_id);
    if call_id is not None:
        try:
            call_status = CallStatus.objects.get(call_id=call_id)
            print("Data is available:", call_status.status)
            return JsonResponse({'status': 'available', 'data': call_status.status})
        except CallStatus.DoesNotExist:
            pass

    # Data is not available yet
    return JsonResponse({'status': 'pending'})

