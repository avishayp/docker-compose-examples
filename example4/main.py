import sys
import os
import json
import redis

rserver = redis.StrictRedis('redis')

# Q methods

Qin = os.environ.get('Qin')
Qout = os.environ.get('Qout')


def pop(qname=Qin):
    _, thing = rserver.brpop(qname)
    return json.loads(str(thing, 'utf-8'))


def push(thing, qname=Qout):
    return rserver.lpush(qname, json.dumps(thing))


def main():
    item = pop() if Qin else 0
    if Qout:
        return push(item + 1)

    # else
    assert item == 2


if __name__ == '__main__':
    main()
