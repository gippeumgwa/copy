import sys
import random
import json

argv = [int(x) for x in sys.argv[1:] if x]
raw = [random.randint(1, 3100) for x in range(15)]
print("::set-output name=topics::"+json.dumps(argv or raw))
