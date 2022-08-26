from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from threading import Thread
import json
import time
import random
import redis

rClient = redis.Redis(host="localhost", port=6379)

def broadcast_change(group_name, payload):
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            payload,
        )
    except Exception as ex:
        print("ex", ex)
        pass


def start_process(*args, **kwargs):
    print(kwargs)
    id = kwargs["id"]
    # reset initially
    rClient.set(id, 0)
    print("starting process.", id)
    for i in range(1, 101):
        r = random.randrange(2, 3)
        time.sleep(r / 10)
        print("POST", i)
        rClient.set(id, i)

        broadcast_change("room", {"type": "process_percent", "percent": i, "id": id})


@csrf_exempt
def ProcessView(request):
    output = {"percent": 0}

    if request.method == "POST":
        print(request.body)
        data = json.loads(request.body)
        kwargs = {"id": data["id"]}
        thread = Thread(target=start_process, args=[], kwargs=kwargs)
        thread.start()

    return JsonResponse(output)
