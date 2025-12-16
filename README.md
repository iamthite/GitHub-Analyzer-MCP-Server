# 🐙 GitHub Analyzer Pro MCP Server v2.0

A **production-ready** Model Context Protocol (MCP) server with **28+ powerful tools** for comprehensive GitHub analysis, built with FastMCP.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.14.0-green)](https://github.com/jlowin/fastmcp)
[![GitHub API](https://img.shields.io/badge/GitHub-API%20v3-black)](https://docs.github.com/rest)
[![Production Ready](https://img.shields.io/badge/status-production--ready-success)](https://github.com)

---

## 🎯 What's New in v2.0

### 🚀 **3X More Tools** - From 9 to 28 Tools!

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Total Tools | 9 | **28** |
| Repository Analysis | Basic | **Advanced with stats & health** |
| Commit Analysis | Simple list | **Detailed + Comparison** |
| Search Capabilities | Basic | **Multi-type (repos/users/topics)** |
| User Features | Profile only | **Profile + Activity + Repos** |
| GitHub Actions | ❌ | **✅ Workflows + Runs** |
| Release Management | ❌ | **✅ Full release tracking** |
| Traffic Analytics | ❌ | **✅ Views + Clones** |
| Community Health | ❌ | **✅ Health metrics** |
| Organization Support | ❌ | **✅ Org profiles** |
| Error Handling | Basic | **Production-grade** |

---

## ✨ Complete Feature Set

### 📦 **Repository Analysis** (8 Tools)
- **get_repository_info** - Complete repo metadata with stats
- **get_repository_languages** - Language breakdown with percentages
- **get_repository_contributors** - Top contributors ranking
- **get_repository_tags** - Release tags listing
- **get_repository_branches** - Branch info with protection status
- **get_repository_stats** - Comprehensive analytics
- **get_repository_traffic** - Views & clones (requires permissions)
- **get_repository_community** - Health score & community files

### 📝 **Commits & History** (3 Tools)
- **get_repository_commits** - Commit history with authors
- **get_commit_details** - Deep dive into specific commits
- **compare_commits** - Compare branches or commits

### 🐛 **Issues & Pull Requests** (3 Tools)
- **get_repository_issues** - Filter by state, labels
- **get_pull_requests** - PR details with merge status
- **get_issue_comments** - Comment threads

### 📁 **Files & Content** (4 Tools)
- **get_file_content** - Read any file from repo
- **get_directory_contents** - Browse directory structure
- **get_repository_readme** - Quick README access
- **search_code** - Find code across repositories

### 🔍 **Search & Discovery** (5 Tools)
- **search_repositories** - Advanced repo search
- **search_users** - Find users & organizations
- **search_topics** - Discover GitHub topics
- **get_trending_repositories** - Hot repos by language
- **get_trending_developers** - Active developers

### 👤 **Users & Organizations** (4 Tools)
- **get_user_profile** - Complete user information
- **get_user_repositories** - User's public repos
- **get_user_activity** - Recent activity feed
- **get_organization_info** - Organization details

### 📦 **Releases & Packages** (2 Tools)
- **get_releases** - All releases with download stats
- **get_latest_release** - Latest release details

### ⚙️ **Workflows & Actions** (2 Tools)
- **get_workflows** - List GitHub Actions workflows
- **get_workflow_runs** - Recent workflow execution history

### 🛠️ **Utilities** (2 Tools)
- **get_rate_limit** - Check API rate limit status
- **server_info** - Server capabilities & stats

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install fastmcp httpx python-dotenv
```

### 2. Set GitHub Token (Recommended)

**Without token:** 60 requests/hour  
**With token:** 5000 requests/hour + full search access

```bash
# Linux/Mac
export GITHUB_TOKEN='ghp_your_token_here'

# Windows PowerShell
$env:GITHUB_TOKEN='ghp_your_token_here'

# Or create .env file
echo "GITHUB_TOKEN=ghp_your_token_here" > .env
```

**Get your token:** https://github.com/settings/tokens
- Required scopes: `public_repo`, `read:user`
- Optional: `repo` (for private repositories)

### 3. Run the Server

```bash
python github_server.py
```

**Expected output:**
```
============================================================
🐙 GitHub Analyzer Pro MCP Server v2.0.0
============================================================

📡 Server Configuration:
   Transport: HTTP
   Host: 0.0.0.0
   Port: 8001
   Timeout: 30.0s

🔑 Authentication:
   GitHub Token: ✓ Configured
   Rate Limit: 5000/hr

📊 Available Tools: 28
   • Repository Analysis (8 tools)
   • Commits & History (3 tools)
   • Issues & PRs (3 tools)
   • Files & Content (4 tools)
   • Search & Discovery (5 tools)
   • Users & Organizations (4 tools)
   • Releases & Packages (2 tools)
   • Workflows & Actions (2 tools)
   • Utilities (2 tools)

✨ Production Features:
   ✓ Enhanced error handling
   ✓ Request caching
   ✓ Rate limit monitoring
   ✓ Community health metrics
   ✓ Traffic analytics
   ✓ GitHub Actions support

🚀 Server Status: READY
   Access at: http://localhost:8001
============================================================
```

---

## 📚 Usage Examples

### 🔍 **Advanced Repository Analysis**

```python
# Get comprehensive stats
{
  "owner": "facebook",
  "repo": "react"
}

# Response includes:
# - Stars, forks, watchers
# - Language breakdown
# - Commit activity
# - Health score
# - Community files
# - Traffic data (if authorized)
```

### 📊 **Language Distribution**

```python
# Get language percentages
{
  "owner": "microsoft",
  "repo": "vscode"
}

# Returns:
# - TypeScript: 45.2%
# - JavaScript: 30.1%
# - CSS: 15.7%
# - etc.
```

### 👥 **Top Contributors**

```python
# See who contributes most
{
  "owner": "torvalds",
  "repo": "linux",
  "limit": 10
}
```

### 🔄 **Compare Branches**

```python
# See what changed between branches
{
  "owner": "python",
  "repo": "cpython",
  "base": "3.11",
  "head": "main"
}

# Shows:
# - Commits ahead/behind
# - Files changed
# - Line additions/deletions
```

### 🐛 **Filter Issues by Labels**

```python
# Find specific issues
{
  "owner": "microsoft",
  "repo": "vscode",
  "state": "open",
  "labels": "bug,high-priority"
}
```

### 📦 **Release Management**

```python
# Get latest release
{
  "owner": "nodejs",
  "repo": "node"
}

# Returns:
# - Version tag
# - Release notes
# - Download links
# - Asset download counts
```

### ⚙️ **Monitor GitHub Actions**

```python
# Check CI/CD status
{
  "owner": "rust-lang",
  "repo": "rust"
}

# See:
# - All workflows
# - Recent runs
# - Success/failure status
```

### 👤 **User Activity Feed**

```python
# What's a user been up to?
{
  "username": "gvanrossum",
  "limit": 20
}

# Shows:
# - Recent commits
# - PRs created
# - Issues opened
# - Repos starred
```

### 🔥 **Discover Trending**

```python
# Hot Python repos this week
{
  "language": "python",
  "since": "weekly"
}
```

### 📈 **Community Health**

```python
# Check repo health
{
  "owner": "django",
  "repo": "django"
}

# Returns:
# - Health percentage
# - README quality
# - Has CODE_OF_CONDUCT
# - Has CONTRIBUTING guide
# - Issue templates
```

---

## 🔧 Connect to Claude Desktop

### Configuration

**macOS:**  
`~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:**  
`%APPDATA%\Claude\claude_desktop_config.json`

**Linux:**  
`~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "github-pro": {
      "url": "http://localhost:8001/mcp/v1"
    }
  }
}
```

**Remote server:**
```json
{
  "mcpServers": {
    "github-pro": {
      "url": "http://your-server-ip:8001/mcp/v1"
    }
  }
}
```

**Restart Claude Desktop** after configuration!

---

## 💬 Talk to Claude

Once connected, ask Claude things like:

```
"Analyze the React repository - give me complete statistics"

"Show me the language breakdown for microsoft/vscode"

"Who are the top 10 contributors to the Linux kernel?"

"Compare the main and develop branches of my-org/my-repo"

"Find all open high-priority bugs in facebook/react"

"What's the latest release of Node.js? Show download counts"

"Are GitHub Actions passing for rust-lang/rust?"

"What has Guido van Rossum been working on lately?"

"Show me trending Rust repositories this month"

"Check the community health score for django/django"

"Search for async functions in the FastAPI codebase"

"Get traffic stats for my repository" (requires auth)

"Show me all workflows and their status for my-org/api"
```

---

## 🏭 Production Features

### ✅ **Enhanced Error Handling**
- Detailed error messages
- Rate limit detection
- Authentication failure handling
- Network timeout management
- Resource not found handling

### ✅ **Performance Optimization**
- Request timeout control (30s)
- Response caching (5min TTL)
- Efficient batch requests
- Maximum result limiting

### ✅ **Security**
- Token-based authentication
- Secure environment variables
- No token logging
- Rate limit compliance

### ✅ **Monitoring & Debugging**
- Rate limit tracking
- Request/response logging
- Server health status
- Detailed tool statistics

### ✅ **Data Quality**
- Response validation
- Safe JSON encoding
- Truncation for large responses
- Binary file handling

---

## 🐳 Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server
COPY github_server.py .

# Environment
ENV GITHUB_TOKEN=""
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import httpx; httpx.get('http://localhost:8001/mcp/v1/health')"

EXPOSE 8001

CMD ["python", "github_server.py"]
```

### requirements.txt

```txt
fastmcp>=2.14.0
httpx>=0.24.0
python-dotenv>=1.0.0
```

### Build & Run

```bash
# Build image
docker build -t github-mcp-pro .

# Run with token
docker run -d \
  -p 8001:8001 \
  -e GITHUB_TOKEN='ghp_your_token' \
  --name github-server \
  --restart unless-stopped \
  github-mcp-pro

# View logs
docker logs -f github-server

# Stop
docker stop github-server
```

### Docker Compose

```yaml
version: '3.8'

services:
  github-mcp:
    build: .
    ports:
      - "8001:8001"
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import httpx; httpx.get('http://localhost:8001/mcp/v1/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## ☁️ Cloud Deployment

### Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up

# Set environment
railway variables set GITHUB_TOKEN=ghp_your_token

# Get URL
railway domain
```

### Deploy to Render

1. Connect your GitHub repository
2. Create new Web Service
3. Set environment variables:
   - `GITHUB_TOKEN`: Your token
4. Build command: `pip install -r requirements.txt`
5. Start command: `python github_server.py`
6. Deploy!

### Deploy to Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch
flyctl launch

# Set secret
flyctl secrets set GITHUB_TOKEN=ghp_your_token

# Deploy
flyctl deploy

# Check status
flyctl status
```

### Deploy to Heroku

```bash
# Create Procfile
echo "web: python github_server.py" > Procfile

# Create app
heroku create github-mcp-pro

# Set token
heroku config:set GITHUB_TOKEN=ghp_your_token

# Deploy
git push heroku main

# Check logs
heroku logs --tail
```

---

## 🔍 Advanced Search Queries

GitHub supports powerful search syntax:

```python
# Search by stars
"query": "web framework stars:>10000"

# Search by language
"query": "machine learning language:python"

# Search by topic
"query": "topic:artificial-intelligence"

# Search by license
"query": "license:mit"

# Search in organization
"query": "org:google android"

# Search by size
"query": "size:>1000 language:go"

# Search by fork count
"query": "forks:>500 language:rust"

# Search by pushed date
"query": "pushed:>2024-01-01"

# Combined
"query": "neural network language:python stars:>1000 topic:deep-learning"
```

---

## 📊 Rate Limit Management

### Check Your Limits

```python
# Use the tool
get_rate_limit()

# Returns:
{
  "core": {
    "limit": 5000,
    "remaining": 4850,
    "reset": "2024-12-15T10:30:00"
  },
  "search": {
    "limit": 30,
    "remaining": 28,
    "reset": "2024-12-15T09:45:00"
  }
}
```

### Best Practices

1. **Use authentication** - 5000 vs 60 requests/hour
2. **Cache results** - Built-in 5-minute caching
3. **Batch requests** - Use higher limits per call
4. **Monitor usage** - Check rate_limit regularly
5. **Handle errors** - Graceful degradation

### Rate Limit Headers

The server automatically handles:
- `X-RateLimit-Limit` - Total limit
- `X-RateLimit-Remaining` - Requests left
- `X-RateLimit-Reset` - Reset timestamp
- `Retry-After` - Seconds to wait

---

## 🛡️ Security Best Practices

### Token Management

```bash
# ✅ DO: Use environment variables
export GITHUB_TOKEN='ghp_...'

# ✅ DO: Use .env file (add to .gitignore)
echo "GITHUB_TOKEN=ghp_..." > .env
echo ".env" >> .gitignore

# ❌ DON'T: Hardcode in files
GITHUB_TOKEN = "ghp_..."  # NEVER DO THIS!

# ❌ DON'T: Commit to git
git add .env  # NEVER DO THIS!
```

### Token Scopes

Minimum required:
- ✅ `public_repo` - Access public repositories
- ✅ `read:user` - Read user profile

Optional for more features:
- `repo` - Access private repositories
- `read:org` - Read organization data
- `admin:repo_hook` - Manage webhooks

### Token Rotation

```bash
# Create new token
1. Visit https://github.com/settings/tokens
2. Generate new token
3. Update environment variable
4. Restart server
5. Revoke old token
```

---

## 🧪 Testing

### Manual Testing

```bash
# Test repository info
curl -X POST http://localhost:8001/mcp/v1/tools/get_repository_info \
  -H "Content-Type: application/json" \
  -d '{"owner": "facebook", "repo": "react"}'

# Test search
curl -X POST http://localhost:8001/mcp/v1/tools/search_repositories \
  -H "Content-Type: application/json" \
  -d '{"query": "fastapi", "limit": 5}'

# Test user profile
curl -X POST http://localhost:8001/mcp/v1/tools/get_user_profile \
  -H "Content-Type: application/json" \
  -d '{"username": "torvalds"}'
```

### Python Testing

```python
import requests

# Test connection
response = requests.post(
    "http://localhost:8001/mcp/v1/tools/server_info",
    json={}
)
assert response.status_code == 200
print(response.json())

# Test repository
response = requests.post(
    "http://localhost:8001/mcp/v1/tools/get_repository_info",
    json={"owner": "python", "repo": "cpython"}
)
data = response.json()
assert "name" in data
print(f"Repository: {data['name']}")
```

---

## 📈 Monitoring & Logging

### Server Logs

The server provides detailed logging:

```
[2024-12-15 10:30:45] INFO - Server started on port 8001
[2024-12-15 10:31:12] INFO - Tool called: get_repository_info
[2024-12-15 10:31:13] INFO - GitHub API request: repos/facebook/react
[2024-12-15 10:31:14] INFO - Response cached for 300s
[2024-12-15 10:31:14] INFO - Tool execution completed: 1.2s
```

### Health Monitoring

```bash
# Check server health
curl http://localhost:8001/health

# Check rate limits
curl -X POST http://localhost:8001/mcp/v1/tools/get_rate_limit \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## 🐛 Troubleshooting

### Common Issues

**"Rate limit exceeded"**
```bash
# Solution: Add GitHub token
export GITHUB_TOKEN='ghp_your_token'
```

**"Repository not found"**
```bash
# Check: Owner and repo spelling
# Check: Repository is public (or token has access)
# Check: Repository hasn't been deleted/renamed
```

**"Connection refused"**
```bash
# Check: Server is running
python github_server.py

# Check: Port 8001 is available
lsof -i :8001  # Linux/Mac
netstat -ano | findstr :8001  # Windows
```

**"Invalid token"**
```bash
# Solution: Regenerate token with correct scopes
# Required: public_repo, read:user
```

**"Timeout error"**
```bash
# Check: Internet connection
# Check: GitHub status: https://www.githubstatus.com/
# Increase: Timeout in code (REQUEST_TIMEOUT)
```

### Debug Mode

```python
# Add to github_server.py for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🎓 Advanced Usage

### Custom Tool Implementation

Add your own tools to `github_server.py`:

```python
@mcp.tool()
@safe_json_response
def your_custom_tool(param: str) -> dict:
    """
    Your custom GitHub tool.
    
    Args:
        param: Parameter description
    
    Returns:
        Custom data
    """
    data = gh_client.request(f"your/endpoint/{param}")
    return {
        "result": data
    }
```

### Batch Processing

```python
# Process multiple repos
repos = [
    ("facebook", "react"),
    ("microsoft", "vscode"),
    ("google", "flutter")
]

for owner, repo in repos:
    info = get_repository_info(owner, repo)
    print(f"{owner}/{repo}: {info['statistics']['stars']} stars")
```

### Caching Strategy

The server includes built-in caching (5 minutes). Customize:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_request(endpoint: str):
    return gh_client.request(endpoint)
```

---

## 📋 Requirements

- **Python:** 3.10 or higher
- **Dependencies:**
  - `fastmcp>=2.14.0`
  - `httpx>=0.24.0`
  - `python-dotenv>=1.0.0`

---

## 🤝 Contributing

Contributions welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch
3. **Add** your improvements
4. **Test** thoroughly
5. **Submit** a pull request

### Ideas for Contributions

- Add more GitHub features
- Implement GraphQL API support
- Add webhook handlers
- Create visualization tools
- Add analytics dashboards
- Improve caching strategies
- Add more search filters
- Enhance error messages
- Add rate limit prediction
- Create CLI interface

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Credits

- **GitHub API** - Data provider
- **FastMCP** - MCP framework
- **Anthropic** - Claude and MCP specification
- **httpx** - HTTP client
- **Contributors** - Thank you!

---

## 📞 Support

- **Documentation:** This README
- **Issues:** [GitHub Issues](https://github.com/yourusername/github-mcp-server/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/github-mcp-server/discussions)
- **API Docs:** [GitHub REST API](https://docs.github.com/rest)

---


## ⭐ Star History

If this project helps you, please consider giving it a ⭐!

---