# Server for final task

This repository contains the python [implementation](server/server.py) of chat-server for final task.

## How to run

### Local run
```python3 server.py```
Requires python >= 3.5.

Server parameters can be configured in [config.py](config.py)

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

<b>Messages would contain only utf-8 characters!</b>

Messages format looks similar to commands format:
```
<packed reciever username length> + <reciever username> + <packed message length> + <message>
```

Example:
```
'Hello, Bob!' for user 'Bob' -> b'\x03\x00\x00\x00Bob\x0b\x00\x00\x00Hello, Bob!'
```

[Python example](client/message_utils.py)

## Commands

After each command you would recieve message.

* `register <username>` - Registration on server. U can't use name of another user.
* `users` - Get list of online users.
* `send <formated message>` - Message sending for specific user.
* `sendall <message>` - Message sending for all online users.
* `recieve` - Recieve all messages that was sended for you. After this command all messages would be removed from server.
Mesages are recieved in specific order: 
```
  1) N = <messages count>
  2) Message 1
     .................................................
N+1) Message N
```
* `logout` - Logout your user. After logouting your profile and your messages would be removed.
