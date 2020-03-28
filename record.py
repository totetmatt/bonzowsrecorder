#!/usr/bin/env python

from collections import namedtuple
import os
import asyncio
import websockets
import json
from git import Repo
import git
import argparse

BASE_REPO_PATH = "repos"
USER_RECORDER_DIR = "{room}-{user}"


Repository = namedtuple('Repository', ['repo', 'dir'])


def getRepo(room, user):
    if not os.path.exists(BASE_REPO_PATH):
        os.mkdir(BASE_REPO_PATH)

    repo_dir = os.path.join(
        BASE_REPO_PATH, USER_RECORDER_DIR.format(room=room, user=user))

    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)

    try:
        return Repository(Repo(repo_dir), repo_dir)
    except git.exc.InvalidGitRepositoryError as InvalidRepo:
        Repo.init(repo_dir, bare=False)
        return Repository(Repo(repo_dir), repo_dir)


async def run(uri, room, user):
    uri = f"{uri}/{room}/{user}"
    repo = getRepo(room, user)
    async with websockets.connect(uri) as websocket:
        while True:
            greeting = await websocket.recv()
            data = json.loads(greeting[:-1])

            if data['Data']['Compile'] == True:
                with open(os.path.join(repo.dir, 'raw.json'), 'w') as f:
                    f.write(greeting[:-1])
                with open(os.path.join(repo.dir, 'code.glsl'), 'w') as f:
                    f.write(data['Data']['Code'])
                repo.repo.index.add(['raw.json', 'code.glsl'])
                repo.repo.index.commit("Update")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Grab and git commit all change from a bonzomatic sender')
    parser.add_argument('--room_name', metavar='room_name', type=str, default="roomtest",
                        help='Room name')
    parser.add_argument('--ws_uri', metavar='ws_uri', type=str, default="ws://drone.alkama.com:9000",
                        help='Room name')
    parser.add_argument('user_name', metavar='user_name', type=str,
                        help='User Name')

    args = parser.parse_args()
    asyncio.get_event_loop().run_until_complete(
        run(uri=args.ws_uri, room=args.room_name, user=args.user_name))
