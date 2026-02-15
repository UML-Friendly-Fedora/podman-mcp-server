# Podman MCP server


## Installation
```bash
# Clone the repository
git clone https://github.com/UML-Friendly-Fedora/podman-mcp-server
cd podman-mcp-server

# Create and activate virtual environment
uv venv
source .venv/bin/activate # On Windows, use: .venv\Scripts\activate

# Install the packages
uv pip install -e .
```

## Usage
Start the mcp server in vscode extensions tab then chat with the build in agent.
For other chat bots use
```bash
uv run podman-mcp
```
