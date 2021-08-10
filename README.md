## FlaskTestApp
Two services generator and invoker.
* generator - generate JSON response with a random value.
* invoker - for find viewer in the local cache (3 keys and TTL 10sec), and find keys in the Redis.

In the invoker Async function run_cascade for 5 different models if the user is not found.
### Start Application
```shell
docker-compose up
```
## Examples for execution using CURL
### ping to generator:

```shell 
 curl -s -w 'Total: %{time_total}\\n' -p http://127.0.0.1:5000/ping
 #pong
```
 
### ping to invoker:
```shell
 curl -s -w 'Total: %{time_total}\\n' -p http://127.0.0.1:5001/ping
 #pong
```
### POST to generator:
```shell
nike@NB02:~$ curl -X POST "http://127.0.0.1:5000?model=1&viewer=nike"
# {"reason": "1", "result": "1"}
```
### GET recomendation from Cache:
```shell
nike@NB02:~$ curl -X GET "http://127.0.0.1:5001/recomended?viewer=nike"
{
  "recommend": [
    {
      "reason": "model1",
      "result": "3"
    },
    {
      "reason": "model2",
      "result": "6"
    },
    {
      "reason": "model3",
      "result": "8"
    },
    {
      "reason": "model4",
      "result": "9"
    },
    {
      "reason": "model5",
      "result": "4"
    }
  ],
  "viewer": "nike"
}
```

### GET recomendation not from Cache:
```shell
nike@NB02:~$ curl -X GET "http://127.0.0.1:5001/recomended?viewer=nike02"
{
  "recommend": [
    {
      "reason": "model1",
      "result": "6"
    },
    {
      "reason": "model2",
      "result": "2"
    },
    {
      "reason": "model3",
      "result": "7"
    },
    {
      "reason": "model4",
      "result": "9"
    },
    {
      "reason": "model5",
      "result": "8"
    }
  ],
  "viewer": "nike02"
}
```
