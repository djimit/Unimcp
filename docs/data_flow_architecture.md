# Unifi MCP Server Data Flow Architecture

This document details the data flows within the Unifi MCP Server, including data models, transformations, and integration points.

## Data Flow Overview

The Unifi MCP Server acts as a bridge between Claude Desktop and the Unifi Site Manager API, transforming natural language requests into structured API calls and converting API responses into user-friendly formats.

```mermaid
flowchart LR
    subgraph "User Interaction"
        NL[Natural Language Request]
        HR[Human-Readable Response]
    end
    
    subgraph "Claude Desktop"
        TP[Tool Processing]
        TR[Tool Response]
    end
    
    subgraph "MCP Server"
        TI[Tool Invocation]
        DT[Data Transformation]
        ER[Error Handling]
        LG[Logging]
    end
    
    subgraph "Unifi API"
        AR[API Request]
        AP[API Response]
    end
    
    NL --> TP
    TP --> TI
    TI --> DT
    DT --> AR
    AR --> AP
    AP --> DT
    DT --> TR
    TR --> HR
    
    ER -.-> DT
    LG -.-> DT
    LG -.-> AR
    LG -.-> AP
    
    classDef user fill:#D4F1F9,stroke:#05445E,stroke-width:2px
    classDef claude fill:#B1D4E0,stroke:#05445E,stroke-width:2px
    classDef mcp fill:#75E6DA,stroke:#05445E,stroke-width:2px
    classDef api fill:#D3D3D3,stroke:#05445E,stroke-width:2px
    
    class NL,HR user
    class TP,TR claude
    class TI,DT,ER,LG mcp
    class AR,AP api
```

## Data Models

### Input Data Models

These models define the structure of data coming into the MCP Server from Claude Desktop.

#### GetSitesInput

```python
class GetSitesInput(BaseModel):
    pass  # No input parameters required
```

#### GetDevicesInput

```python
class GetDevicesInput(BaseModel):
    site_id: str = Field(..., description="ID of the site to get devices for")
```

#### GetClientsInput

```python
class GetClientsInput(BaseModel):
    site_id: str = Field(..., description="ID of the site to get clients for")
```

### Output Data Models

These models define the structure of data going out from the MCP Server to Claude Desktop.

#### GetSitesOutput

```python
class GetSitesOutput(BaseModel):
    sites: List[Dict[str, Any]] = Field(..., description="List of Unifi sites")
```

Example:
```json
{
  "sites": [
    {
      "id": "site1",
      "name": "Main Office"
    },
    {
      "id": "site2",
      "name": "Branch Office"
    }
  ]
}
```

#### GetDevicesOutput

```python
class GetDevicesOutput(BaseModel):
    devices: List[Dict[str, Any]] = Field(
        ...,
        description="List of devices for the specified site"
    )
```

Example:
```json
{
  "devices": [
    {
      "id": "device1",
      "name": "AP-Office",
      "type": "UAP-AC-Pro",
      "status": "connected"
    },
    {
      "id": "device2",
      "name": "Switch-Main",
      "type": "USW-Pro-24-PoE",
      "status": "connected"
    }
  ]
}
```

#### GetClientsOutput

```python
class GetClientsOutput(BaseModel):
    clients: List[Dict[str, Any]] = Field(
        ...,
        description="List of clients for the specified site"
    )
```

Example:
```json
{
  "clients": [
    {
      "id": "client1",
      "name": "Laptop-1",
      "ip": "192.168.1.100",
      "mac": "00:11:22:33:44:55"
    },
    {
      "id": "client2",
      "name": "Phone-1",
      "ip": "192.168.1.101",
      "mac": "AA:BB:CC:DD:EE:FF"
    }
  ]
}
```

### Unifi API Data Models

These models represent the data structures used by the Unifi Site Manager API.

#### Site

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "role": "string",
  "status": "string"
}
```

#### Device

```json
{
  "id": "string",
  "name": "string",
  "type": "string",
  "model": "string",
  "mac": "string",
  "ip": "string",
  "status": "string",
  "uptime": "number",
  "last_seen": "string",
  "firmware_version": "string"
}
```

#### Client

```json
{
  "id": "string",
  "name": "string",
  "mac": "string",
  "ip": "string",
  "hostname": "string",
  "os_name": "string",
  "device_type": "string",
  "is_wired": "boolean",
  "last_seen": "string",
  "uptime": "number",
  "signal_strength": "number"
}
```

## Data Transformations

### Natural Language to Tool Invocation

Claude Desktop transforms natural language requests into structured tool invocations:

```mermaid
flowchart LR
    NL[Natural Language Request] --> NLU[Natural Language Understanding]
    NLU --> TI[Tool Identification]
    TI --> PE[Parameter Extraction]
    PE --> TV[Tool Invocation]
    
    classDef nlp fill:#FFD700,stroke:#B8860B,stroke-width:2px
    
    class NL,NLU,TI,PE,TV nlp
```

Example:
```
Natural Language: "Show me all devices at my Main Office site"

Tool Invocation: {
  "tool": "get_devices",
  "parameters": {
    "site_id": "site1"
  }
}
```

### Tool Invocation to API Request

The MCP Server transforms tool invocations into Unifi API requests:

```mermaid
flowchart LR
    TI[Tool Invocation] --> PI[Parameter Interpretation]
    PI --> VC[Validation & Conversion]
    VC --> AR[API Request Formation]
    AR --> AE[API Endpoint Call]
    
    classDef transform fill:#90EE90,stroke:#006400,stroke-width:2px
    
    class TI,PI,VC,AR,AE transform
```

Example:
```
Tool Invocation: {
  "tool": "get_devices",
  "parameters": {
    "site_id": "site1"
  }
}

API Request:
GET https://api.ui.com/sites/site1/devices
Headers: {
  "Authorization": "Bearer unifi_api_key",
  "Content-Type": "application/json"
}
```

### API Response to Tool Response

The MCP Server transforms Unifi API responses into tool responses:

```mermaid
flowchart LR
    AR[API Response] --> PD[Parse Data]
    PD --> FD[Filter Data]
    FD --> TD[Transform Data]
    TD --> VM[Validate Model]
    VM --> TR[Tool Response]
    
    classDef transform fill:#90EE90,stroke:#006400,stroke-width:2px
    
    class AR,PD,FD,TD,VM,TR transform
```

Example:
```
API Response:
[
  {
    "id": "device1",
    "name": "AP-Office",
    "type": "UAP-AC-Pro",
    "model": "UAP-AC-Pro",
    "mac": "00:11:22:33:44:55",
    "ip": "192.168.1.10",
    "status": "connected",
    "uptime": 1234567,
    "last_seen": "2023-01-01T00:00:00Z",
    "firmware_version": "5.60.9"
  },
  ...
]

Tool Response:
{
  "devices": [
    {
      "id": "device1",
      "name": "AP-Office",
      "type": "UAP-AC-Pro",
      "status": "connected"
    },
    ...
  ]
}
```

### Tool Response to Natural Language

Claude Desktop transforms tool responses into natural language responses:

```mermaid
flowchart LR
    TR[Tool Response] --> DP[Data Processing]
    DP --> CG[Content Generation]
    CG --> NLG[Natural Language Generation]
    NLG --> HR[Human-Readable Response]
    
    classDef nlp fill:#FFD700,stroke:#B8860B,stroke-width:2px
    
    class TR,DP,CG,NLG,HR nlp
```

Example:
```
Tool Response:
{
  "devices": [
    {
      "id": "device1",
      "name": "AP-Office",
      "type": "UAP-AC-Pro",
      "status": "connected"
    },
    {
      "id": "device2",
      "name": "Switch-Main",
      "type": "USW-Pro-24-PoE",
      "status": "connected"
    }
  ]
}

Human-Readable Response:
"I found 2 devices at your Main Office site:

1. AP-Office (UAP-AC-Pro) - Status: connected
2. Switch-Main (USW-Pro-24-PoE) - Status: connected

All devices are currently connected and operational."
```

## Data Flow Sequences

### Get Sites Sequence

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Desktop
    participant MCP as MCP Server
    participant Unifi as Unifi API
    
    User->>Claude: "Show me all my Unifi sites"
    Claude->>MCP: Tool Invocation: get_sites
    MCP->>Unifi: GET /sites
    Unifi->>MCP: Sites JSON Response
    MCP->>Claude: GetSitesOutput
    Claude->>User: "Here are your Unifi sites: Main Office, Branch Office"
```

### Get Devices Sequence

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Desktop
    participant MCP as MCP Server
    participant Unifi as Unifi API
    
    User->>Claude: "Show me all devices at my Main Office"
    Claude->>MCP: Tool Invocation: get_devices(site_id="site1")
    MCP->>Unifi: GET /sites/site1/devices
    Unifi->>MCP: Devices JSON Response
    MCP->>Claude: GetDevicesOutput
    Claude->>User: "Here are the devices at Main Office: AP-Office, Switch-Main"
```

### Get Clients Sequence

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Desktop
    participant MCP as MCP Server
    participant Unifi as Unifi API
    
    User->>Claude: "Show me all clients at my Main Office"
    Claude->>MCP: Tool Invocation: get_clients(site_id="site1")
    MCP->>Unifi: GET /sites/site1/clients
    Unifi->>MCP: Clients JSON Response
    MCP->>Claude: GetClientsOutput
    Claude->>User: "Here are the clients at Main Office: Laptop-1, Phone-1"
```

## Error Handling Data Flow

```mermaid
sequenceDiagram
    participant Claude as Claude Desktop
    participant MCP as MCP Server
    participant Unifi as Unifi API
    
    Claude->>MCP: Tool Invocation
    
    alt API Key Missing
        MCP->>MCP: Check API Key
        MCP->>Claude: HTTP 500 - API Key Missing
    else API Connection Error
        MCP->>Unifi: API Request
        Unifi->>MCP: Connection Error
        MCP->>Claude: HTTP 500 - Connection Error
    else API Authentication Error
        MCP->>Unifi: API Request
        Unifi->>MCP: HTTP 401 - Unauthorized
        MCP->>Claude: HTTP 500 - Authentication Error
    else API Response Error
        MCP->>Unifi: API Request
        Unifi->>MCP: HTTP 4xx/5xx Error
        MCP->>Claude: HTTP 500 - API Error
    else Data Processing Error
        MCP->>Unifi: API Request
        Unifi->>MCP: JSON Response
        MCP->>MCP: Process Data (Error)
        MCP->>Claude: HTTP 500 - Processing Error
    end
```

## Logging Data Flow

```mermaid
flowchart TD
    subgraph "MCP Server"
        SI[Server Initialization] --> LL[Log Level]
        LL --> LF[Log Format]
        
        TI[Tool Invocation] --> LR[Log Request]
        AR[API Request] --> LA[Log API Call]
        AP[API Response] --> LP[Log Response]
        ER[Error] --> LE[Log Error]
        
        LR --> LO[Log Output]
        LA --> LO
        LP --> LO
        LE --> LO
        
        LO --> LC[Console Logger]
        LO --> LF[File Logger]
    end
    
    classDef init fill:#D4F1F9,stroke:#05445E,stroke-width:2px
    classDef event fill:#B1D4E0,stroke:#05445E,stroke-width:2px
    classDef log fill:#75E6DA,stroke:#05445E,stroke-width:2px
    classDef output fill:#D3D3D3,stroke:#05445E,stroke-width:2px
    
    class SI,LL,LF init
    class TI,AR,AP,ER event
    class LR,LA,LP,LE log
    class LO,LC,LF output
```

## Data Storage Considerations

The Unifi MCP Server is primarily stateless, with no persistent data storage requirements. However, there are some considerations for ephemeral data:

### Logging

- **Console Logging**: Default logging to console
- **File Logging**: Optional logging to files
- **Docker Volume**: When using Docker, logs can be persisted using volumes

### Environment Variables

- **`.env` File**: Stores configuration like API keys
- **Environment Variables**: Can be set directly in the environment
- **Docker Environment**: Set via docker-compose.yml or command line

### Caching Considerations (Future Enhancement)

While not implemented in the current version, future enhancements could include caching:

```mermaid
flowchart LR
    subgraph "MCP Server"
        AR[API Request] --> CC[Check Cache]
        CC --> CR{Cache Hit?}
        CR -->|Yes| CD[Cache Data]
        CR -->|No| AP[API Call]
        AP --> ND[New Data]
        ND --> UC[Update Cache]
        UC --> RD[Return Data]
        CD --> RD
    end
    
    classDef request fill:#D4F1F9,stroke:#05445E,stroke-width:2px
    classDef cache fill:#B1D4E0,stroke:#05445E,stroke-width:2px
    classDef api fill:#75E6DA,stroke:#05445E,stroke-width:2px
    classDef response fill:#D3D3D3,stroke:#05445E,stroke-width:2px
    
    class AR request
    class CC,CR,CD,UC cache
    class AP,ND api
    class RD response
```

## Integration Points

### Claude Desktop Integration

```mermaid
flowchart LR
    subgraph "Claude Desktop"
        CD[Claude Desktop]
        CF[Config File]
    end
    
    subgraph "MCP Server"
        MS[MCP Server]
        TS[Tool Schema]
        RS[Resource Schema]
    end
    
    CF -->|Configures| CD
    CD -->|Discovers| TS
    CD -->|Discovers| RS
    CD -->|Invokes| MS
    
    classDef claude fill:#D4F1F9,stroke:#05445E,stroke-width:2px
    classDef mcp fill:#B1D4E0,stroke:#05445E,stroke-width:2px
    
    class CD,CF claude
    class MS,TS,RS mcp
```

### Unifi API Integration

```mermaid
flowchart LR
    subgraph "MCP Server"
        UC[Unifi Client]
        AK[API Key]
    end
    
    subgraph "Unifi API"
        SE[Sites Endpoint]
        DE[Devices Endpoint]
        CE[Clients Endpoint]
    end
    
    AK -->|Authenticates| UC
    UC -->|Requests| SE
    UC -->|Requests| DE
    UC -->|Requests| CE
    
    classDef mcp fill:#D4F1F9,stroke:#05445E,stroke-width:2px
    classDef api fill:#B1D4E0,stroke:#05445E,stroke-width:2px
    
    class UC,AK mcp
    class SE,DE,CE api
```

## Data Security Considerations

### API Key Protection

```mermaid
flowchart TD
    subgraph "Environment"
        EV[Environment Variable]
        EF[.env File]
    end
    
    subgraph "MCP Server"
        UC[Unifi Client]
        LG[Logger]
    end
    
    subgraph "API Request"
        HD[Headers]
        BD[Body]
    end
    
    EV -->|Loads| UC
    EF -->|Loads| UC
    UC -->|Sets| HD
    UC -.->|Doesn't Log| LG
    
    classDef env fill:#D4F1F9,stroke:#05445E,stroke-width:2px
    classDef server fill:#B1D4E0,stroke:#05445E,stroke-width:2px
    classDef request fill:#75E6DA,stroke:#05445E,stroke-width:2px
    
    class EV,EF env
    class UC,LG server
    class HD,BD request
```

### Data Sanitization

```mermaid
flowchart LR
    subgraph "API Response"
        AR[API Response]
    end
    
    subgraph "Data Processing"
        FD[Filter Data]
        SD[Sanitize Data]
        VD[Validate Data]
    end
    
    subgraph "Tool Response"
        TR[Tool Response]
    end
    
    AR --> FD
    FD --> SD
    SD --> VD
    VD --> TR
    
    classDef api fill:#D4F1F9,stroke:#05445E,stroke-width:2px
    classDef process fill:#B1D4E0,stroke:#05445E,stroke-width:2px
    classDef tool fill:#75E6DA,stroke:#05445E,stroke-width:2px
    
    class AR api
    class FD,SD,VD process
    class TR tool
```

## Conclusion

The data flow architecture of the Unifi MCP Server is designed to efficiently transform natural language requests into structured API calls and convert API responses into user-friendly formats. The system is primarily stateless, with clear data models and transformations at each stage of the process.

Key aspects of the data flow architecture include:

1. **Well-defined Data Models**: Clear input and output models for each tool
2. **Transformation Pipelines**: Structured processes for converting between different data formats
3. **Error Handling**: Comprehensive error detection and reporting
4. **Logging**: Detailed logging throughout the system
5. **Security**: Protection of sensitive data like API keys

This architecture provides a solid foundation for the Unifi MCP Server, enabling it to reliably bridge the gap between natural language interaction and the Unifi Site Manager API.
