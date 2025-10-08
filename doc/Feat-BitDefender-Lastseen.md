# check lastseen status

check lastseen status according the the endpoint list.

## cli

### critical

```
check_bitdefender lastseen -d machine.domain.tld
```
result
```
DEFENDER CRITICAL - Host not found (machine.domain.tld) | lastseen=999;7;15
```

### warning


```
check_bitdefender lastseen -d machine.domain.tld
```

```
DEFENDER WARNING - Host onboarded, not seen > 7 days (machine.domain.tld)  | lastseen=7;7;15
```


### OK


```
check_bitdefender lastseen -d machine.domain.tld
```

```
DEFENDER OK - Host onboarded (machine.domain.tld) | lastseen=0;7;15
```

