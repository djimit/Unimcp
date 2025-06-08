# Unifi MCP Server Architecture

## System Overview

The Unifi MCP Server architecture enables natural language interaction with Unifi network infrastructure through Claude Desktop by implementing the Model Context Protocol (MCP). This document outlines the system's components, interactions, data flows, and deployment considerations.

## Architecture Principles

1. **Separation of Concerns**: Clear boundaries between components with well-defined responsibilities
2. **API-First Design**: RESTful interfaces for all components
3. **Security by Design**: Secure authentication and data handling throughout
4. **Scalability**: Components designed to scale independently
5. **Extensibility**: Easy addition of new tools and capabilities

## Component Architecture

```mermaid
graph TD
    subgraph "Client Layer"
        CD[Claude Desktop]
    end

    subgraph "MCP Server Layer"
        MS[MCP Server]
        FW[FastAPI Web Server]
        TC[Tool Controller]
        RC[Resource Controller]
    end

    subgraph "Integration Layer"
        UC[Unifi Client]
        EM[Error Manager]
        LM[Logging Manager]
    end

    subgraph "External Systems"
        UA[Unifi API]
    end

    CD <--> FW
    FW <--> MS
    MS <--> TC
    MS <--> RC
    TC <--> UC
    RC <--> UC
    UC <--> EM
    UC <--> LM
    UC <--> UA

    classDef clientLayer fill:#D4F1F9,stroke:#05445E,stroke-width:2px
    classDef mcpLayer fill:#B1D4E0,stroke:#05445E,stroke-width:2px
    classDef integrationLayer fill:#75E6DA,stroke:#05445E,stroke-width:2px
    classDef externalLayer fill:#D3D3D3,stroke:#05445E,stroke-width:2px

    class CD clientLayer
    class MS,FW,TC,RC mcpLayer
    class UC,EM,LM integrationLayer
    class UA externalLayer
```

### Component Descriptions

#### Client Layer

- **Claude Desktop**: AI assistant that interacts with users via natural language and communicates with the MCP Server

#### MCP Server Layer

- **MCP Server**: Core component implementing the Model Context Protocol
- **FastAPI Web Server**: Handles HTTP requests and responses
- **Tool Controller**: Manages MCP tools (get_sites, get_devices, get_clients)
- **Resource Controller**: Manages MCP resources (unifi://sites)

#### Integration Layer

- **Unifi Client**: Handles communication with the Unifi Site Manager API
- **Error Manager**: Handles and standardizes error responses
- **Logging Manager**: Manages logging throughout the system

#### External Systems

- **Unifi API**: External Unifi Site Manager API

## Data Flow Architecture

### Primary Data Flows

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Desktop
    participant MCP as MCP Server
    participant Unifi as Unifi Client
    participant API as Unifi API

    User->>Claude: Natural language request
    Claude->>MCP: Tool invocation request
    MCP->>Unifi: API request
    Unifi->>API: HTTP request with API key
    API->>Unifi: JSON response
    Unifi->>MCP: Processed data
    MCP->>Claude: Formatted response
    Claude->>User: Natural language response
```

### Authentication Flow

```mermaid
sequenceDiagram
    participant MCP as MCP Server
    participant Unifi as Unifi Client
    participant API as Unifi API

    Note over MCP,API: API Key Authentication
    
    MCP->>Unifi: Initialize with API key
    Unifi->>Unifi: Validate API key exists
    Unifi->>API: Request with API key in header
    API->>API: Validate API key
    API->>Unifi: Authentication response
    Unifi->>MCP: Authentication status
```

## Detailed Component Design

### MCP Server Component

```mermaid
classDiagram
    class MCPServer {
        +name: string
        +description: string
        +app: FastAPI
        +tool(name, input_model, output_model, description)
        +resource(uri)
    }
    
    class Tool {
        +name: string
        +input_model: BaseModel
        +output_model: BaseModel
        +description: string
        +handler: function
    }
    
    class Resource {
        +uri: string
        +handler: function
    }
    
    MCPServer "1" *-- "many" Tool
    MCPServer "1" *-- "many" Resource
```

### Unifi Client Component

```mermaid
classDiagram
    class UnifiClient {
        +api_key: string
        +base_url: string
        +get_sites()
        +get_devices(site_id)
        +get_clients(site_id)
    }
    
    class Site {
        +id: string
        +name: string
    }
    
    class Device {
        +id: string
        +name: string
        +type: string
        +status: string
    }
    
    class Client {
        +id: string
        +name: string
        +ip: string
        +mac: string
    }
    
    UnifiClient ..> Site : returns
    UnifiClient ..> Device : returns
    UnifiClient ..> Client : returns
```

## API Design

### MCP Tools API

| Tool Name | Description | Input | Output |
|-----------|-------------|-------|--------|
| `get_sites` | Get a list of all Unifi sites | None | List of sites with IDs and names |
| `get_devices` | Get a list of devices for a specific site | Site ID | List of devices with details |
| `get_clients` | Get a list of clients for a specific site | Site ID | List of clients with details |

### MCP Resources API

| Resource URI | Description | Output |
|--------------|-------------|--------|
| `unifi://sites` | Resource for accessing Unifi sites | List of sites with IDs and names |

### REST API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/docs` | GET | OpenAPI documentation |
| `/openapi.json` | GET | OpenAPI specification |
| `/mcp/tools` | GET | List of available MCP tools |
| `/mcp/tools/{tool_name}` | POST | Execute an MCP tool |
| `/mcp/resources/{resource_uri}` | GET | Access an MCP resource |

## Deployment Architecture

### Standard Deployment

```mermaid
graph TD
    subgraph "User Environment"
        CD[Claude Desktop]
        MS[MCP Server]
    end
    
    subgraph "External Systems"
        UA[Unifi API]
    end
    
    CD <--> MS
    MS <--> UA
    
    classDef userEnv fill:#D4F1F9,stroke:#05445E,stroke-width:2px
    classDef external fill:#D3D3D3,stroke:#05445E,stroke-width:2px
    
    class CD,MS userEnv
    class UA external
```

### Docker Deployment

```mermaid
graph TD
    subgraph "User Environment"
        CD[Claude Desktop]
    end
    
    subgraph "Docker Environment"
        DC[Docker Container]
        MS[MCP Server]
    end
    
    subgraph "External Systems"
        UA[Unifi API]
    end
    
    CD <--> DC
    DC --> MS
    MS <--> UA
    
    classDef userEnv fill:#D4F1F9,stroke:#05445E,stroke-width:2px
    classDef dockerEnv fill:#B1D4E0,stroke:#05445E,stroke-width:2px
    classDef external fill:#D3D3D3,stroke:#05445E,stroke-width:2px
    
    class CD userEnv
    class DC,MS dockerEnv
    class UA external
```

### Enterprise Deployment with OAuth

```mermaid
graph TD
    subgraph "User Environment"
        CD[Claude Desktop]
    end
    
    subgraph "Azure Cloud"
        APIM[API Management]
        EID[Entra ID]
        AZ[Azure Functions]
        MS[MCP Server]
    end
    
    subgraph "External Systems"
        UA[Unifi API]
    end
    
    CD <--> APIM
    APIM <--> EID
    APIM <--> AZ
    AZ --> MS
    MS <--> UA
    
    classDef userEnv fill:#D4F1F9,stroke:#05445E,stroke-width:2px
    classDef azureEnv fill:#B1D4E0,stroke:#05445E,stroke-width:2px
    classDef external fill:#D3D3D3,stroke:#05445E,stroke-width:2px
    
    class CD userEnv
    class APIM,EID,AZ,MS azureEnv
    class UA external
```

## Security Architecture

### Authentication and Authorization

```mermaid
graph TD
    subgraph "Authentication"
        AK[API Key]
        OH[OAuth 2.0]
    end
    
    subgraph "Authorization"
        RP[Resource Permissions]
        SC[Scope Control]
    end
    
    subgraph "Data Protection"
        ET[Encryption in Transit]
        ER[Encryption at Rest]
    end
    
    AK --> RP
    OH --> SC
    RP --> ET
    SC --> ET
    ET --> ER
    
    classDef auth fill:#FFD700,stroke:#B8860B,stroke-width:2px
    classDef authz fill:#FFA500,stroke:#B8860B,stroke-width:2px
    classDef protect fill:#FF8C00,stroke:#B8860B,stroke-width:2px
    
    class AK,OH auth
    class RP,SC authz
    class ET,ER protect
```

### Security Considerations

1. **API Key Protection**:
   - Store API keys securely in environment variables
   - Rotate keys regularly
   - Use the principle of least privilege

2. **Transport Security**:
   - Use HTTPS for all communications
   - Implement proper certificate validation

3. **Error Handling**:
   - Sanitize error messages to prevent information leakage
   - Log detailed errors internally but return generic messages to clients

4. **Enterprise Security**:
   - Implement OAuth 2.0 with Azure API Management and Entra ID
   - Use token-based authentication with short-lived tokens
   - Implement proper scope control

## Scalability and Performance

### Scalability Considerations

```mermaid
graph TD
    subgraph "Vertical Scaling"
        WC[Worker Count]
        MU[Memory Usage]
    end
    
    subgraph "Horizontal Scaling"
        LB[Load Balancing]
        DC[Docker Containers]
    end
    
    subgraph "Performance Optimization"
        CA[Caching]
        CO[Connection Pooling]
    end
    
    WC --> LB
    MU --> DC
    LB --> CA
    DC --> CO
    
    classDef vertical fill:#98FB98,stroke:#006400,stroke-width:2px
    classDef horizontal fill:#90EE90,stroke:#006400,stroke-width:2px
    classDef performance fill:#3CB371,stroke:#006400,stroke-width:2px
    
    class WC,MU vertical
    class LB,DC horizontal
    class CA,CO performance
```

### Performance Considerations

1. **Caching**:
   - Implement caching for frequently accessed data
   - Use time-based cache invalidation

2. **Connection Pooling**:
   - Reuse HTTP connections to the Unifi API
   - Implement proper connection timeout handling

3. **Asynchronous Processing**:
   - Use async/await for I/O-bound operations
   - Implement proper error handling for async operations

4. **Worker Configuration**:
   - Adjust the number of workers based on system resources
   - Monitor worker performance and adjust as needed

## Extension Points

The architecture is designed to be extensible in the following ways:

1. **Additional MCP Tools**:
   - Add new tools to support more Unifi API functionality
   - Implement tools for specific use cases (e.g., network troubleshooting)

2. **Additional MCP Resources**:
   - Add new resources to provide more data to Claude Desktop
   - Implement resources for specific data types (e.g., network statistics)

3. **Integration with Other Systems**:
   - Extend the architecture to support other network management systems
   - Implement adapters for different API formats

4. **Enhanced Security**:
   - Add support for additional authentication methods
   - Implement more granular authorization controls

## Architecture Decision Records

### ADR-1: Use of FastAPI for Web Framework

**Context**: We need a web framework to handle HTTP requests and responses.

**Decision**: Use FastAPI as the web framework.

**Rationale**:
- FastAPI provides automatic OpenAPI documentation
- It has built-in support for Pydantic models
- It supports asynchronous request handling
- It has good performance characteristics

**Consequences**:
- Requires Python 3.6+ (we're using 3.8+)
- Adds a dependency on Pydantic for data validation

### ADR-2: Use of Environment Variables for Configuration

**Context**: We need a way to configure the server without hardcoding values.

**Decision**: Use environment variables for configuration, with support for .env files.

**Rationale**:
- Environment variables are a standard way to configure applications
- They can be set in different ways (shell, .env file, Docker)
- They don't require code changes to update

**Consequences**:
- Requires documentation of available environment variables
- Requires handling of missing or invalid environment variables

### ADR-3: Docker Support

**Context**: We need a way to deploy the server in different environments.

**Decision**: Provide Docker support with a Dockerfile and docker-compose.yml.

**Rationale**:
- Docker provides a consistent deployment environment
- It simplifies dependency management
- It makes it easier to deploy in different environments

**Consequences**:
- Requires Docker knowledge to use
- Adds complexity to the deployment process
- Requires proper volume mapping for logs

## Conclusion

The Unifi MCP Server architecture provides a robust, secure, and extensible foundation for integrating Unifi network infrastructure with Claude Desktop. By implementing the Model Context Protocol, it enables natural language interaction with Unifi systems, making network management more accessible and intuitive.

The architecture is designed to be deployed in various environments, from a simple local installation to a more complex enterprise deployment with OAuth authentication. It provides clear separation of concerns, well-defined interfaces, and extension points for future enhancements.
