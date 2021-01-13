import sys
import random
import json

argv = [int(x) for x in sys.argv[1:] if x]
raw = [random.randint(1, 3300) for x in range(20)]
print("::set-output name=topics::"+json.dumps(argv or raw))
