# check onboading status

check onboarding status according the the endpoint list.

## cli

### critical

```
check_bitdefender onboarding -d machine.domain.tld
```
result
```
DEFENDER CRITICAL - Host not found (machine.domain.tld) | onboarding=0;7;15
```

### warning


```
check_bitdefender onboarding -d machine.domain.tld
```

```
DEFENDER WARNING - Host onboarded, not seen > 7 days (machine.domain.tld)  | onboarding=0;7;15
```


### OK


```
check_bitdefender onboarding -d machine.domain.tld
```

```
DEFENDER OK - Host onboarded (machine.domain.tld) | onboarding=0;7;15
```

