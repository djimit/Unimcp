# Unifi MCP Server Architecture Documentation

## Overview

This document serves as the central index for the Unifi MCP Server architecture documentation. It provides an overview of the architectural design and links to detailed documentation on specific aspects of the architecture.

The Unifi MCP Server is a Model Context Protocol (MCP) server that integrates with the Unifi Site Manager API, allowing users to interact with their Unifi network infrastructure using natural language through Claude Desktop.

## Architecture Documentation Map

```mermaid
mindmap
  root((Unifi MCP Server Architecture))
    Component Architecture
      System Components
      Component Interactions
      Deployment Options
    Data Flow Architecture
      Data Models
      Transformations
      Storage Considerations
    Security Architecture
      Authentication
      Authorization
      Data Protection
      Threat Model
    Integration Architecture
      Claude Desktop Integration
      Unifi API Integration
      Extension Points
```

## Core Architecture Documents

| Document | Description | Key Sections |
|----------|-------------|--------------|
| [Architecture Overview](architecture.md) | Comprehensive overview of the system architecture | Component Architecture, Deployment Architecture, Security Architecture |
| [Data Flow Architecture](data_flow_architecture.md) | Detailed documentation of data flows within the system | Data Models, Data Transformations, Data Storage |
| [Security Architecture](security_architecture.md) | Security aspects of the system | Authentication, Data Protection, Threat Model |
| [Integration Architecture](integration_architecture.md) | Integration with external systems | Claude Desktop Integration, Unifi API Integration |

## Component Architecture

The Unifi MCP Server consists of several key components that work together to provide the functionality:

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

For detailed information on the component architecture, see the [Architecture Overview](architecture.md) document.

## Data Flow Architecture

The data flow architecture describes how data moves through the system, from natural language requests to API calls and back:

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

For detailed information on the data flow architecture, see the [Data Flow Architecture](data_flow_architecture.md) document.

## Security Architecture

The security architecture addresses authentication, authorization, data protection, and threat modeling:

```mermaid
graph TD
    subgraph "Security Layers"
        AL[Authentication Layer]
        TL[Transport Layer]
        DL[Data Layer]
        CL[Code Layer]
        OL[Operational Layer]
    end
    
    AL --> TL
    TL --> DL
    DL --> CL
    CL --> OL
    
    classDef security fill:#FF6B6B,stroke:#A30000,stroke-width:2px
    
    class AL,TL,DL,CL,OL security
```

For detailed information on the security architecture, see the [Security Architecture](security_architecture.md) document.

## Integration Architecture

The integration architecture describes how the MCP server integrates with Claude Desktop and the Unifi API:

```mermaid
graph LR
    subgraph "User Environment"
        CD[Claude Desktop]
    end
    
    subgraph "Integration Layer"
        MCP[MCP Server]
    end
    
    subgraph "External Systems"
        UA[Unifi API]
        FI[Future Integrations]
    end
    
    CD <--> MCP
    MCP <--> UA
    MCP <-.-> FI
    
    classDef user fill:#D4F1F9,stroke:#05445E,stroke-width:2px
    classDef integration fill:#B1D4E0,stroke:#05445E,stroke-width:2px
    classDef external fill:#75E6DA,stroke:#05445E,stroke-width:2px
    
    class CD user
    class MCP integration
    class UA,FI external
```

For detailed information on the integration architecture, see the [Integration Architecture](integration_architecture.md) document.

## Deployment Architecture

The Unifi MCP Server can be deployed in various configurations:

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

### Enterprise Deployment

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

For detailed information on deployment options, see the [Architecture Overview](architecture.md) document.

## Architecture Decision Records

The architecture is based on several key decisions:

1. **Use of FastAPI**: FastAPI was chosen as the web framework for its automatic OpenAPI documentation, built-in support for Pydantic models, and asynchronous request handling.

2. **Environment Variables for Configuration**: Environment variables were chosen for configuration to avoid hardcoding values and to support different deployment environments.

3. **Docker Support**: Docker support was added to provide a consistent deployment environment and simplify dependency management.

For detailed information on architecture decisions, see the [Architecture Overview](architecture.md#architecture-decision-records) section.

## Extension Points

The architecture is designed to be extensible in several ways:

1. **Additional MCP Tools**: New tools can be added to support more Unifi API functionality.

2. **Additional MCP Resources**: New resources can be added to provide more data to Claude Desktop.

3. **Integration with Other Systems**: The architecture can be extended to support other systems beyond Unifi.

For detailed information on extension points, see the [Integration Architecture](integration_architecture.md#integration-extensibility) section.

## Future Architecture Considerations

Future enhancements to the architecture may include:

1. **Enhanced Authentication**: OAuth integration and multi-factor authentication.

2. **Caching**: Implementation of caching for frequently accessed data.

3. **Event-Driven Architecture**: Support for real-time updates based on events from the Unifi system.

4. **Scalability Enhancements**: Additional measures to improve scalability for larger deployments.

For detailed information on future considerations, see the respective sections in the architecture documents.

## Related Documentation

- [Project Overview](1_overview_project.md)
- [Installation and Setup](2_installation_setup.md)
- [Configuration Guide](3_configuration_guide.md)
- [Usage Guide](4_usage_guide.md)
- [API Reference](5_api_reference.md)
- [Docker Deployment](6_docker_deployment.md)
- [Troubleshooting Guide](7_troubleshooting_guide.md)
- [Maintenance and Updates](8_maintenance_updates.md)