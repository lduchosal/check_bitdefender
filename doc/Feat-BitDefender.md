# Feature Specification: Endpoint ID Lookup by Computer DNS Name

## Overview
This feature enables the retrieval of endpoint IDs from BitDefender GravityZone for Endpoint by using the computer's DNS name (FQDN). This is essential for correlating endpoints across different monitoring systems and performing targeted security operations.

## Purpose
- Resolve endpoint DNS names to unique BitDefender GravityZone endpoint IDs
- Enable cross-referencing between DNS-based identification and Defender's internal endpoint tracking
- Support automated security workflows that start with DNS names but need endpoint IDs for Defender API operations

## Business Use Case
Security teams often have DNS names of endpoints from network monitoring tools, log files, or incident reports, but need the corresponding BitDefender GravityZone endpoint ID to:
- Query endpoint-specific security data
- Retrieve vulnerability information
- Check onboarding status
- Perform security actions

## API Requirements

### Authentication
- **Required**: Azure AD Application Registration with appropriate permissions
- **Scopes**: `WindowsDefenderATP` or `https://securitycenter.onmicrosoft.com/windowsdefenderatp/.default`
- **Permissions**: `Endpoint.Read.All` (minimum required)

### Geographic Endpoints
The BitDefender GravityZone for Endpoint API has different endpoints based on geographic location:
- **EU**: `https://api-eu.securitycenter.microsoft.com`
- **EU3**: `https://api-eu3.securitycenter.microsoft.com` (used in this example)
- **US**: `https://cloudgz.gravityzone.bitdefender.com/api/`
- **UK**: `https://api-uk.securitycenter.microsoft.com`

## API Implementation

### Endpoint
```
GET https://api-eu3.securitycenter.microsoft.com/api/endpoints
```

### Query Parameters
- **Filter by computerDnsName**: `$filter=computerDnsName eq 'fqdn'`
- **Select only the id**: `$select=id`

### Complete Query
```
https://api-eu3.securitycenter.microsoft.com/api/endpoints?$filter=computerDnsName eq 'fqdn'&$select=id
```

### Headers
```http
Authorization: Bearer {access_token}
Content-Type: application/json
```

### Expected Response
```json
{
  "@odata.context": "https://api-eu3.securitycenter.microsoft.com/api/$metadata#Endpoints(id)",
  "value": [
    {
      "id": "89xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx1f"
    }
  ]
}
```

### Extracted Endpoint ID
```
89xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx1f
```

## Implementation Details

### Modified Files
- **core/defender.py**: Added `get_endpoint_by_dns_name()` method to DefenderClient class for DNS name to endpoint ID resolution using Microsoft Graph API deviceManagement endpoint with deviceName filter.

### Migration Checklist: Microsoft Graph API to MS Defender API

**API Migration Tasks:**

1. ✅ **Change base_url from Microsoft Graph to MS Defender API endpoint**
   - From: `https://graph.microsoft.com/v1.0`
   - To: `https://api-eu3.securitycenter.microsoft.com` (or configurable geographic endpoint)

2. ✅ **Update get_endpoint_by_dns_name() method to use /api/endpoints endpoint**
   - From: `/deviceManagement/managedDevices`
   - To: `/api/endpoints`

3. ✅ **Change filter parameter from deviceName to computerDnsName**
   - From: `$filter=deviceName eq '{dns_name}'`
   - To: `$filter=computerDnsName eq '{dns_name}'`

4. ✅ **Update get_endpoint_by_id() method to use MS Defender endpoints endpoint**
   - From: `/deviceManagement/managedDevices/{endpoint_id}`
   - To: `/api/endpoints/{endpoint_id}`

5. ✅ **Fix get_endpoint_vulnerabilities() method endpoint path**
   - From: `/security/endpoints/{endpoint_id}/vulnerabilities`
   - To: `/api/endpoints/{endpoint_id}/vulnerabilities`

6. ✅ **Update authentication scope from Graph to WindowsDefenderATP**
   - From: `https://graph.microsoft.com/.default`
   - To: `https://securitycenter.onmicrosoft.com/windowsdefenderatp/.default`

7. ✅ **Add geographic endpoint configuration support**
   - Support EU, EU3, US, UK endpoints
   - Make base_url configurable in constructor

8. ✅ **Update error handling for MS Defender API responses**
   - Handle MS Defender-specific error responses
   - Update exception messages for context