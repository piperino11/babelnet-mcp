# BabelNet MCP Server

A Model Context Protocol (MCP) server providing access to BabelNet's multilingual semantic network. Query concepts, retrieve synsets, explore semantic relations, and get multilingual translations through BabelNet's comprehensive knowledge base.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start Guide

Get up and running with BabelNet MCP in 5 minutes!

## Prerequisites

- Python 3.10 or higher
- pip package manager
- A BabelNet API key ([register here](https://babelnet.org/register))

## Step-by-Step Installation

### 1. Get Your API Key

```bash
# Visit https://babelnet.org/register and sign up
# You'll receive your API key via email within minutes
```

### 2. Clone and Install

```bash
# Clone the repository
git clone https://github.com/piperino11/babelnet-mcp.git
cd babelnet-mcp


# Install the package
pip install -e .
```

### 3. Configure BabelNet

```bash
# Create configuration file
cat > babelnet_conf.yml << EOF
RESTFUL_KEY: 'paste-your-api-key-here'
EOF
```

### 4. Test the Installation

```bash
# Run the server
babelnet-mcp
```

You should see:
```
🚀 Starting BabelNet MCP Server...
⚠️  NOTE: Each query consumes 1 Babelcoin (limit: 1000/day)
✅ Server ready - waiting for connections...
```

### 5. Configure Claude Desktop

This is an example. For more information refear to https://modelcontextprotocol.io/docs/develop/connect-local-servers

**macOS:**
```bash
# Open the config file
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```cmd
# Open the config file
notepad %APPDATA%\Claude\claude_desktop_config.json
```

**Add this configuration:**
```json
{
  "mcpServers": {
    "babelnet": {
      "command": "babelnet-mcp --api-key paste-your-api-key-here"
    }
  }
}
```

### 6. Restart Claude Desktop

Close and reopen Claude Desktop completely.

## 🎯 First Query

Try asking Claude:

> "Find all the meanings of the word 'bank'."


## 💰 API Limits

- **Free Tier**: 1000 Babelcoins per day
- **Cost**: 1 query = 1 Babelcoin
- **Reset**: Daily at midnight UTC
- **Increase Limit**: For research purposes, request an increase at [BabelNet](https://babelnet.org/login)
- **Commercial Use**: Contact [Babelscape](https://babelscape.com) for commercial licensing

## 📄 License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This is an unofficial MCP server for BabelNet. BabelNet is a product of [Babelscape](https://babelscape.com).

The server is provided "as is" without warranty of any kind. The authors are not responsible for:
- API costs or limits
- Data accuracy
- Service availability
- Any damages from using this software
