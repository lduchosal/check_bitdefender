# Detail of an endpoint

https://www.bitdefender.com/business/support/en/77209-128476-network.html
## request
```
  {
       "params": {
           "endpointId" : "54a28b41b1a43d89367b23fd",
           "options": {
               "includeScanLogs": true  
            }
       },
       "jsonrpc": "2.0",
       "method": "getManagedEndpointDetails",
       "id": "301f7b05-ec02-481b-9ed6-c07b97de2b7b"
  }  
```

## response
```
  {
      "id":"0df7568c-59c1-48e0-a31b-18d83e6d9810",
      "jsonrpc":"2.0",
      "result": {
          'id': '54a28b41b1a43d89367b23fd',
          'name': 'WIN-TGQDU499RS4',
          'companyId': '5575a235d2172c65038b454e',
          'operatingSystem': 'Windows Server 2008 R2 Datacenter',
          'state': 1,
          'ip': '10.10.24.154',
          'lastSeen': '2015-06-22T13:46:59',
          'machineType': 1,
          'agent': {
               'engineVersion': '7.61184',
               'primaryEngine': 1,
               'fallbackEngine': 2,
               'lastUpdate': '2015-06-22T13:40:06',
               'licensed': 1,
               'productOutdated': False,
               'productUpdateDisabled': False,
               'productVersion': '6.2.3.569',
               'signatureOutdated': False,
               'signatureUpdateDisabled': False,
               'type': 3
           },
          'group': {
               'id': '5575a235d2172c65038b456d',
               'name': 'Custom Groups'
           },
          'malwareStatus': {
               'detection': False,
               'infected': False
           },
          'modules': {
               'advancedThreatControl': False,
               'antimalware': True,
               'contentControl': False,
               'deviceControl': False,
               'firewall': False,
               'powerUser': False,
               'networkAttackDefense': False
               'integrityMonitoring: False,
           },
          'policy': {
               'id': '5121da426803fa2d0e000017',
               'applied': True,
               'name': 'Default policy'
           },
           "label" : "endpoint label",
           "moveState": 1,
           "riskScore": {
                "value": "81%",
                "impact": "High",
                "misconfigurations": "70%",
                "appVulnerabilities": "11%",
                "humanRisks": "19%"
           },
        "lastSuccessfulScan": {
                "name": "72OHI5dnIH",
                "date": "2023-07-19T04:09:29+00:00"
           },

      }
  }   
```
## cli

```
check_bitdefender detail -d machine.domain.tld
```
result
```
DEFENDER OK - Host found (machine.domain.tld) 
id: 54a28b41b1a43d89367b23fd
name: WIN-TGQDU499RS4
operatingSystem: Windows Server 2008 R2 Datacenter
lastSeen: 2015-06-22T13:46:59
lastSuccessfulScan: 2023-07-19T04:09:29+00:00
malwareStatus_detection: false
malwareStatus_infected: false
riskScore: 81%
| detail=1;0;0
```
