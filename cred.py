import sys
from urllib.parse import urlparse

def urlparse_or_none(x):
    try:
        return urlparse(x)
    except:
        return None

argv = [urlparse_or_none(x) for x in sys.argv[1:] if x]
secrets = {y for x in argv if x for y in (x.username, x.password) if y}
a = [print('::add-mask::%s' % x) for x in secrets]
