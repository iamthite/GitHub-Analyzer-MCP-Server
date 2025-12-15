# 🐙 GitHub Analyzer MCP Server

A powerful Model Context Protocol (MCP) server built with **FastMCP** that provides comprehensive GitHub repository analysis, code search, issue tracking, and statistics.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.14.0-green)](https://github.com/jlowin/fastmcp)
[![GitHub API](https://img.shields.io/badge/GitHub-API%20v3-black)](https://docs.github.com/rest)

## ✨ Features

This FastMCP server provides **9 powerful GitHub tools**:

| Tool | Description | Use Cases |
|------|-------------|-----------|
| 🔍 **get_repository_info** | Full repo details | Stars, forks, language, license, stats |
| 🔎 **search_repositories** | Find repos by query | Discover projects, filter by language |
| 📜 **get_repository_commits** | Recent commit history | Track changes, view authors |
| 🐛 **get_repository_issues** | Open/closed issues | Bug tracking, feature requests |
| 📄 **get_file_content** | Read file from repo | View code, documentation |
| 👤 **get_user_profile** | User information | Followers, repos, bio |
| 🔥 **get_trending_repositories** | Trending repos | Discover popular projects |
| 💻 **search_code** | Find code snippets | Search across all repos |
| ℹ️ **server_info** | Server details | Tools, features, limits |

## 🎯 Why Use This Server?

- ✅ **No GitHub Account Needed** - Works without authentication (60 req/hr)
- ✅ **Higher Limits with Token** - 5000 req/hr with GitHub token
- ✅ **Comprehensive Analysis** - Get all repo data in seconds
- ✅ **Code Search** - Find code across millions of repositories
- ✅ **Real-time Data** - Direct from GitHub API
- ✅ **Easy Integration** - Works with Claude Desktop

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install fastmcp httpx python-dotenv
```

### 2. Optional: Get GitHub Token (Recommended)

**Why?** Without token: 60 requests/hour. With token: 5000 requests/hour!

1. Go to [GitHub Settings → Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes: `public_repo`, `read:user`
4. Copy your token

**Set the token:**
```bash
# Linux/Mac
export GITHUB_TOKEN='ghp_your_token_here'

# Windows (PowerShell)
$env:GITHUB_TOKEN='ghp_your_token_here'
```

**Or create `.env` file:**
```
GITHUB_TOKEN=ghp_your_token_here
```

### 3. Run the Server

```bash
python github_server.py
```

**Output:**
```
🐙 Starting GitHub Analyzer MCP Server...
📡 Transport: HTTP
🌐 Host: 0.0.0.0
🔌 Port: 8001
🔑 GitHub Token: ✓ Set

📝 Available tools: 9
🚀 Server ready! Access at http://localhost:8001
```

### 4. Test It

```bash
# Get repo info
curl -X POST http://localhost:8001/mcp/v1/tools/get_repository_info \
  -H "Content-Type: application/json" \
  -d '{"owner": "openai", "repo": "whisper"}'
```

## 📚 Tool Examples

### 1️⃣ Analyze a Repository

```python
# Input
{
  "owner": "facebook",
  "repo": "react"
}

# Output
{
  "name": "facebook/react",
  "description": "A JavaScript library for building user interfaces",
  "statistics": {
    "stars": 225000,
    "forks": 45000,
    "open_issues": 850
  },
  "language": "JavaScript",
  "license": "MIT License"
}
```

### 2️⃣ Search Repositories

```python
# Input
{
  "query": "machine learning language:python",
  "sort": "stars",
  "limit": 5
}

# Output
{
  "total_count": 125000,
  "repositories": [
    {
      "name": "tensorflow/tensorflow",
      "stars": 182000,
      "language": "Python"
    },
    ...
  ]
}
```

### 3️⃣ Get Recent Commits

```python
# Input
{
  "owner": "torvalds",
  "repo": "linux",
  "limit": 5
}

# Output
{
  "commits": [
    {
      "sha": "abc1234",
      "message": "Fix memory leak in driver",
      "author": "Linus Torvalds",
      "date": "2024-12-14T10:30:00Z"
    },
    ...
  ]
}
```

### 4️⃣ View Issues

```python
# Input
{
  "owner": "microsoft",
  "repo": "vscode",
  "state": "open",
  "limit": 5
}

# Output
{
  "issues": [
    {
      "number": 12345,
      "title": "Feature request: Dark mode improvements",
      "state": "open",
      "comments": 15,
      "labels": ["feature-request", "enhancement"]
    },
    ...
  ]
}
```

### 5️⃣ Read File Content

```python
# Input
{
  "owner": "python",
  "repo": "cpython",
  "path": "README.rst",
  "branch": "main"
}

# Output
{
  "path": "README.rst",
  "size": 5432,
  "content": "This is the Python programming language...",
  "url": "https://github.com/python/cpython/blob/main/README.rst"
}
```

### 6️⃣ Get User Profile

```python
# Input
{
  "username": "torvalds"
}

# Output
{
  "username": "torvalds",
  "name": "Linus Torvalds",
  "bio": "Creator of Linux",
  "statistics": {
    "public_repos": 6,
    "followers": 180000,
    "following": 0
  }
}
```

### 7️⃣ Search Code

```python
# Input
{
  "query": "async def process",
  "owner": "fastapi",
  "limit": 5
}

# Output
{
  "total_count": 234,
  "results": [
    {
      "name": "main.py",
      "path": "app/main.py",
      "repository": "fastapi/fastapi",
      "url": "https://github.com/..."
    },
    ...
  ]
}
```

## 💬 Usage with Claude

Once connected to Claude Desktop, ask:

```
"Analyze the React repository"
"Find Python machine learning repositories with most stars"
"Show me recent commits in the Linux kernel"
"What are the open issues in VSCode?"
"Get the README from tensorflow/tensorflow"
"Who is the creator of Linux on GitHub?"
"Search for async functions in FastAPI repository"
"What are today's trending Python repositories?"
```

## 🔌 Connect to Claude Desktop

### Configuration File:

**MacOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "github": {
      "url": "http://localhost:8001/mcp/v1"
    }
  }
}
```

**For remote server:**
```json
{
  "mcpServers": {
    "github": {
      "url": "http://your-server-ip:8001/mcp/v1"
    }
  }
}
```

Then restart Claude Desktop!

## 🔑 GitHub Token Setup

### Why You Need a Token

| Feature | Without Token | With Token |
|---------|---------------|------------|
| Rate Limit | 60 req/hour | 5000 req/hour |
| Search | Limited | Full access |
| Private Repos | ❌ No | ✅ Yes (if token has access) |

### Create Token

1. **Visit:** https://github.com/settings/tokens
2. **Click:** "Generate new token (classic)"
3. **Name:** "MCP Server Token"
4. **Select Scopes:**
   - ✅ `public_repo` - Access public repositories
   - ✅ `read:user` - Read user profile
   - ✅ `repo` - Access private repos (optional)
5. **Generate** and copy token
6. **Set environment variable** (see Quick Start)

### Security Note

⚠️ **Never commit your token to git!**
- Use environment variables
- Use `.env` file (add to `.gitignore`)
- Rotate tokens periodically

## 🐳 Docker Deployment

### Dockerfile:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN pip install fastmcp httpx python-dotenv

COPY github_server.py .

ENV GITHUB_TOKEN=""

EXPOSE 8001

CMD ["python", "github_server.py"]
```

### Build & Run:

```bash
docker build -t github-mcp-server .

docker run -d \
  -p 8001:8001 \
  -e GITHUB_TOKEN='your_token_here' \
  --name github-server \
  github-mcp-server
```

## ☁️ Deploy to Cloud

### Heroku:

```bash
echo "web: python github_server.py" > Procfile
heroku create github-mcp-server
heroku config:set GITHUB_TOKEN=your_token
git push heroku main
```

### Railway.app:

```bash
railway login
railway init
railway up
railway variables set GITHUB_TOKEN=your_token
```

### Render.com:

1. Connect GitHub repo
2. Set environment variable: `GITHUB_TOKEN`
3. Deploy automatically

## 🔧 Advanced Usage

### Search Query Syntax

GitHub supports advanced search:

```python
# Search by language
"query": "machine learning language:python"

# Search by stars
"query": "web framework stars:>10000"

# Search by topic
"query": "topic:artificial-intelligence"

# Search by license
"query": "license:mit"

# Search in specific org
"query": "org:google android"

# Combined
"query": "neural network language:python stars:>1000"
```

### Error Handling

All tools return errors as JSON:

```json
{
  "error": "Repository not found: owner/repo"
}
```

Common errors:
- `404` - Repository/user not found
- `403` - Rate limit exceeded (add token!)
- `401` - Invalid token
- Network errors - Check connection

## 📊 Rate Limits

### Without Authentication:
- 60 requests per hour
- IP-based tracking

### With GitHub Token:
- 5,000 requests per hour
- Account-based tracking

### Check Your Limit:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.github.com/rate_limit
```

## 🛠️ Development

### Project Structure:

```
github-mcp-server/
├── github_server.py      # Main FastMCP server
├── requirements.txt      # Dependencies
├── README.md            # This file
├── .env.example         # Token template
├── .gitignore          # Git ignore
└── Dockerfile          # Docker config
```

### Adding New Tools:

```python
@mcp.tool()
def your_new_tool(param: str) -> str:
    """
    Tool description.
    
    Args:
        param: Parameter description
        
    Returns:
        JSON string with results
    """
    try:
        data = make_github_request(f"endpoint/{param}")
        result = {"data": data}
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)
```

## 🧪 Testing

```python
import requests

# Test repository info
response = requests.post(
    "http://localhost:8001/mcp/v1/tools/get_repository_info",
    json={"owner": "openai", "repo": "gpt-3"}
)
print(response.json())
```

## 🔍 Troubleshooting

### "Rate limit exceeded"
**Solution:** Add GitHub token for 5000 req/hr limit

### "Repository not found"
**Solution:** Check owner/repo spelling, verify it's public

### "Invalid token"
**Solution:** Regenerate token with correct scopes

### Server won't start
**Solution:** Check port 8001 is free, verify dependencies installed

## 📖 API Reference

- [GitHub REST API Documentation](https://docs.github.com/rest)
- [GitHub Search Syntax](https://docs.github.com/search-github/searching-on-github)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

## 🤝 Contributing

Contributions welcome! Ideas:
- Add pull request analysis
- Add repository statistics graphs
- Add webhook support
- Add commit comparison
- Add more search filters

## 📄 License

MIT License - See LICENSE file

## 🙏 Credits

- [GitHub API](https://docs.github.com/rest) - Data provider
- [FastMCP](https://github.com/jlowin/fastmcp) - MCP framework
- [Anthropic](https://www.anthropic.com/) - Claude and MCP

---

**Built with 🐙 for GitHub enthusiasts**

**⭐ Star this repo if helpful!**