#!/usr/bin/env python3
import os
import sys
import random
import subprocess
import tempfile
import datetime
import hashlib
import requests

# follows tasks done by NewDockerReplicaBase

env = os.environ

username = env.get('DOCKER_USERNAME')

subprocess.Popen([
    'docker', 'login',
    '--username', username,
    '--password', env.get('DOCKER_PASSWORD'),
], stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()

prefix = 'data'


def make_dockerfile(repo):
    return """
        FROM alpine
        RUN apk add --no-cache git && \
            mkdir -p /root/repo && \
            git clone %s /root/repo --bare && \
            ls /root/repo
    """ % repo


workdir = tempfile.mkdtemp('frt', 'newdocker')
gh = [
    "hash1145148101919",
    "jurassic8101919",
    "informational1919810",
    "stripe334hanshin",
    "monetary114514",
    "gnol-akirneh",
    "rolyatn",
]

for num in [int(x) for x in sys.argv[1:]]:
    gh_name = gh[max(num - 1, 0) // 500]
    r = requests.get('https://github.com/%s/%s-%d/raw/master/manifest' % (gh_name, prefix, num))
    if r.status_code != 200:
        print('Status code %d' % r.status_code)
        manifest_hash = '0000000000000000000000000000000000000000000000000000000000000000'
    else:
        m = hashlib.sha256()
        m.update(r.content)
        digest = m.digest()
        manifest_hash = digest.hex()
    print('Manifest hash was %s' % manifest_hash)
    dest = "%s/%s-%d:v2-%s-%s" % (
        username, prefix,
        num, datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S"),
        manifest_hash
    )
    with open(os.path.join(workdir, 'Dockerfile'), 'w') as f:
        f.write(make_dockerfile('https://github.com/%s/%s-%d.git' % (gh_name, prefix, num)))
    subprocess.Popen([
        'docker', 'build', '.', '-t', dest,
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=workdir).wait()
    subprocess.Popen([
        'docker', 'push', dest,
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=workdir).wait()
    subprocess.Popen([
        'docker', 'rmi', dest,
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=workdir).wait()
