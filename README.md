# Bonzo WS Recorder

## Setup

- Git
- Python 3

Install python via `pip install -r req.txt`

## Usage

```
usage: record.py [-h] [--room_name room_name] user_name

Grab and git commit all change from a bonzomatic sender

positional arguments:
  user_name             User Name

optional arguments:
  -h, --help            show this help message and exit
  --room_name room_name
                        Room name
```

Recorded git will be in `./repos/{roomname}-{username}/`

Example after manual push to github : https://github.com/totetmatt/bonzo-testroom-totetmatt
