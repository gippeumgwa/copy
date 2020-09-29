#!/usr/bin/env python3
import os
import random
import subprocess
import tempfile
import time

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

for num in [random.randint(1, 3100) for x in range(5)]:
    print(num)
    gh_name = gh[max(num - 1, 0) // 500]
    dest = "%s/%s-%d:v2-%d-%s" % (
        username, prefix,
        num, int(round(time.time() * 1000)),
        None
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
