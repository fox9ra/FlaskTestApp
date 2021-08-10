import json
import asyncio
import httpx
import itertools

from flask import Flask, request
from cachetools import TTLCache
from redis import Redis

local_cache = TTLCache(maxsize=10, ttl=360)
redis_cache = Redis(host='redis', port=6379)

models = ['model1', 'model2', 'model3', 'model4', 'model5']
url = "http://generator:5000/"

#get value from cache
def get_key(viewer):
    if viewer in local_cache:
        return local_cache[viewer]
    else:
        redis_value = redis_cache.get(viewer)
        if redis_value is None:
            key_value = None
        else:
            key_value = json.loads(redis_value.decode())
        return key_value

#send value to cache
def cache(key, value):
    #print("Cache", key, value)
    local_cache[key] = value
    redis_cache.set(key, json.dumps(value))

def async_call(viewer):
    event_loop = asyncio.new_event_loop()
    result = event_loop.run_until_complete(call_url_async(viewer, models))
    return result

async def call_url_async(viewer, models):
    async with httpx.AsyncClient() as client:
        return await asyncio.gather(
            *map(call_url, models, itertools.repeat(viewer), itertools.repeat(client),)
        )

async def call_url(model, viewer, httpx_client):
    response = await httpx_client.post(url, params={'model': model, 'viewer': viewer})
    return response.json()

#cascade function
def run_cascade(viewer):
    #print("Cascade")
    result = async_call(viewer)
    return {'viewer': viewer, 'recommend': result}

# create the Flask app
app = Flask(__name__)

# tell Flask to use the above defined config

@app.get('/ping')
def ping():
    return 'pong'

@app.route('/recomended', methods=['GET'])
def recommended():
    viewer = request.args.get('viewer')
    cached_value = get_key(viewer)
    if not cached_value:
        #print("toCascade", viewer)
        recommend = run_cascade(viewer)
        cache(viewer, recommend)
        return recommend
    else:
        return cached_value

if __name__ == '__main__':
    # run app in debug mode on port 5001
    app.run(debug=True, host='0.0.0.0', port=5000)