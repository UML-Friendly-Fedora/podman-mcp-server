package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net"
	"net/http"
	"os"
	"time"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type ListContainersArgs struct {
	All bool `json:"all" jsonschema:"Show all containers (default shows just running)"`
}

func main() {
	socketPath := "/run/user/1000/podman/podman.sock"

	// HTTP client using Unix socket
	httpClient := &http.Client{
		Timeout: 10 * time.Second,
		Transport: &http.Transport{
			DialContext: func(ctx context.Context, network, addr string) (net.Conn, error) {
				return net.Dial("unix", socketPath)
			},
		},
	}

	// Create server
	server := mcp.NewServer(&mcp.Implementation{
		Name:    "podman-mcp-server",
		Version: "1.0.0",
	}, &mcp.ServerOptions{})

	// Add tool using the generic AddTool function
	mcp.AddTool(server, &mcp.Tool{
		Name:        "list_containers",
		Description: "List Podman containers using the Podman API",
	}, func(ctx context.Context, req *mcp.CallToolRequest, args ListContainersArgs) (*mcp.CallToolResult, any, error) {
		
		url := "http://localhost/v4.9.3/libpod/containers/json"
		if args.All {
			url += "?all=true"
		}

		httpReq, err := http.NewRequestWithContext(ctx, "GET", url, nil)
		if err != nil {
			return &mcp.CallToolResult{
				Content: []mcp.Content{
					&mcp.TextContent{Text: fmt.Sprintf("Error creating request: %v", err)},
				},
				IsError: true,
			}, nil, nil
		}

		resp, err := httpClient.Do(httpReq)
		if err != nil {
			return &mcp.CallToolResult{
				Content: []mcp.Content{
					&mcp.TextContent{Text: fmt.Sprintf("Error connecting to Podman: %v", err)},
				},
				IsError: true,
			}, nil, nil
		}
		defer resp.Body.Close()

		if resp.StatusCode < 200 || resp.StatusCode > 299 {
			return &mcp.CallToolResult{
				Content: []mcp.Content{
					&mcp.TextContent{Text: fmt.Sprintf("Podman API error: %s", resp.Status)},
				},
				IsError: true,
			}, nil, nil
		}

		var result any
		err = json.NewDecoder(resp.Body).Decode(&result)
		if err != nil {
			return &mcp.CallToolResult{
				Content: []mcp.Content{
					&mcp.TextContent{Text: fmt.Sprintf("Error decoding response: %v", err)},
				},
				IsError: true,
			}, nil, nil
		}

		// Format the result as JSON
		jsonData, err := json.MarshalIndent(result, "", "  ")
		if err != nil {
			return &mcp.CallToolResult{
				Content: []mcp.Content{
					&mcp.TextContent{Text: fmt.Sprintf("Error formatting response: %v", err)},
				},
				IsError: true,
			}, nil, nil
		}

		return &mcp.CallToolResult{
			Content: []mcp.Content{
				&mcp.TextContent{Text: string(jsonData)},
			},
		}, nil, nil
	})

	fmt.Fprintln(os.Stderr, "Podman MCP server running on stdio...")

	// Run the server on stdio transport
	if err := server.Run(context.Background(), &mcp.StdioTransport{}); err != nil {
		panic(err)
	}
}