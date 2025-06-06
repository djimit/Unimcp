# Usage Guide

This guide explains how to use the Unifi MCP Server with Claude Desktop to interact with your Unifi network using natural language.

## Prerequisites

Before using the Unifi MCP Server with Claude Desktop, ensure:

1. The Unifi MCP Server is [installed and set up](2_installation_setup.md)
2. The server is running (via `start_server.sh`, `start_server.bat`, or Docker)
3. Claude Desktop is [configured](3_configuration_guide.md) to connect to the server

## Available Tools

The Unifi MCP Server provides the following tools:

| Tool | Description | Input | Output |
|------|-------------|-------|--------|
| `get_sites` | Get a list of all Unifi sites | None | List of sites with IDs and names |
| `get_devices` | Get a list of devices for a specific site | Site ID | List of devices with details |
| `get_clients` | Get a list of clients for a specific site | Site ID | List of clients with details |

## Using Claude Desktop with Unifi MCP Server

### Starting a Conversation

1. Open Claude Desktop
2. Start a new conversation
3. You should see the Unifi tools available in the interface

### Natural Language Queries

You can interact with your Unifi network using natural language. Here are some example queries:

#### Getting Sites

```
Show me all my Unifi sites
```

```
List all the Unifi sites I have access to
```

```
What Unifi sites do I have?
```

Claude will use the `get_sites` tool to retrieve and display a list of your Unifi sites.

#### Getting Devices

```
Show me all devices at my Main Office site
```

```
What devices are connected to site1?
```

```
List all the access points and switches at my Branch Office
```

Claude will use the `get_devices` tool to retrieve and display a list of devices for the specified site.

#### Getting Clients

```
Show me all clients connected to my Main Office site
```

```
Who is connected to site1 right now?
```

```
List all the devices connected to my Branch Office network
```

Claude will use the `get_clients` tool to retrieve and display a list of clients for the specified site.

### Combining Queries

You can also ask more complex questions that combine multiple tools:

```
Show me all devices at my Main Office and tell me how many clients are connected to each
```

```
Compare the number of clients between my Main Office and Branch Office sites
```

Claude will use multiple tools to gather the necessary information and provide a comprehensive response.

## Understanding the Results

### Site Information

When you request site information, you'll receive data like:

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

### Device Information

When you request device information, you'll receive data like:

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

### Client Information

When you request client information, you'll receive data like:

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

## Advanced Usage

### Filtering and Searching

You can ask Claude to filter or search the results:

```
Show me all offline devices at my Main Office
```

```
Find all clients with IP addresses in the 192.168.1.x range
```

```
Which access points have the most clients connected?
```

### Troubleshooting with Claude

You can use Claude to help troubleshoot network issues:

```
Are there any disconnected devices at my Main Office?
```

```
Check if client Laptop-1 is connected to my network
```

```
When was the last time Phone-1 connected to my network?
```

## Best Practices

1. **Be Specific**: When asking about devices or clients, specify which site you're interested in
2. **Use Site Names**: You can refer to sites by their names (e.g., "Main Office") rather than IDs
3. **Ask Follow-up Questions**: If you need more details, ask Claude follow-up questions
4. **Verify Important Information**: For critical operations, verify the information with your Unifi console

## Limitations

The current implementation has some limitations:

1. **Read-Only Operations**: The MCP server currently only supports read operations (getting information)
2. **Limited Historical Data**: The server doesn't provide historical data or trends
3. **No Real-time Updates**: The data is fetched when requested and doesn't update in real-time

## Next Steps

- Explore the [API Reference](5_api_reference.md) for more details on available tools
- Learn about [Docker Deployment](6_docker_deployment.md) for containerized environments
- Check the [Troubleshooting Guide](7_troubleshooting_guide.md) if you encounter any issues