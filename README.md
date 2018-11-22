# Server for final task

This repository contains the python [implementation](server/server.py) of chat-server for final task.

## How to run

### Local run
```
cd server
python3 server.py
```
Requires python >= 3.5.

Server parameters can be configured in [config.py](server/config.py)

## Commands format

All commands to server should be packed:
```
<packed command length> + <command> 
[+ <packed argument length> + <argument>]
[+ ... ]
```

Exmaples: 
```
users -> b'\x05\x00\x00\x00users'
register Bob -> b'\x08\x00\x00\x00register\x03\x00\x00\x00Bob'
```

[Python example](client/command_utils.py)

## Messages format

<b>Messages shouldn't be greater then 60 characters!</b>

Messages format looks similar to commands format:
```
<packed receiver username length> + <receiver username> + <packed message length> + <message>
```

Example:
```
'Hello, Bob!' for user 'Bob' -> b'\x03\x00\x00\x00Bob\x0b\x00\x00\x00Hello, Bob!'
```

[Python example](client/message_utils.py)

## Commands

After each command you would receive message.

* `register <username>` - Registration on server. U can't use name of another user. <b>Username shouldn't be greater then 8 symbols</b>
* `users` - Get list of online users.
* `send <formated message>` - Message sending for specific user.
* `sendall <message>` - Message sending for all online users.
* `receive` - receive all messages that was sended for you. After this command all messages would be removed from server.
Mesages are received in specific order: 
```
  1) N = <messages count>
  2) Message 1
     .................................................
N+1) Message N
```
* `logout` - Logout your user. After logouting your profile and your messages would be removed.
