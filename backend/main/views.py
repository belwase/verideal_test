from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from threading import Thread
import json
import time
import random
import redis

rClient = redis.Redis(
    host='localhost',
    port=6379
)

def start_process(*args, **kwargs):
    print(kwargs)
    id = kwargs['id']
    # reset initially
    rClient.set(id, 0)
    print("starting process.", id)
    for i in range(1, 101):
        r = random.randrange(2, 3)
        time.sleep(r/10)
        print("POST", i)
        rClient.set(id, i)



@csrf_exempt
def ProcessView(request):
    output = {'percent': 0}
    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            percent = rClient.get(id)
            print("GET", percent)
            if percent:
                output['percent'] = int(percent);

    elif request.method == 'POST':
        print(request.body)
        data = json.loads(request.body)
        kwargs = {
            "id": data["id"]
        }
        thread = Thread(
            target=start_process,
            args=[],
            kwargs=kwargs
        )
        thread.start()

    return JsonResponse(output)
