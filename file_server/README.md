# myftp1.0

There are 3 types of command in this protocol
1. put
2. get
3. list

## PUT

```
put "file.txt"

request:
0000 0000 <followed by null-terminating string> 0000 0000 <binary data>...

response:
0000 0000 (success)
0000 0001 (error)
```

## GET

```
get "file.txt"

request:
0010 0000 <followed by null-terminating string> 0000 0000

response:
0000 0000 <binary data> (sucess)
0000 0001 (error)
```

## LIST

```
list

request:
0100 0000

response:
0000 0000 <null-terminated string> 0000 0000 <null-terminate string>... EOF (success)
0000 0001 (error)
```