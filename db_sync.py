import time
import redis


def decoy()
	while True:
    		r = redis.Redis(host='localhost', port=26379)
    		print(r.get('key'))
    		time.sleep(100)


decoy()
