#!/usr/bin/env python3
"""
GitHub MCP Server using FastMCP
Analyze GitHub repositories, search code, view issues, and get repository statistics
"""

from fastmcp import FastMCP
import httpx
import os
import json
from typing import Optional
from datetime import datetime
import base64

# Initialize FastMCP server
mcp = FastMCP("GitHub-Analyzer-MCP-Server")

# GitHub configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")  # Optional but recommended for higher rate limits
GITHUB_API_BASE = "https://api.github.com"

def make_github_request(endpoint: str, params: dict = None, method: str = "GET") -> dict:
    """Make authenticated request to GitHub API"""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    
    url = f"{GITHUB_API_BASE}/{endpoint}"
    
    try:
        with httpx.Client(timeout=30.0) as client:
            if method == "GET":
                response = client.get(url, params=params, headers=headers)
            elif method == "POST":
                response = client.post(url, json=params, headers=headers)
            
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise Exception(f"Repository or resource not found: {endpoint}")
        elif e.response.status_code == 403:
            raise Exception(f"Rate limit exceeded or access forbidden. Consider adding GITHUB_TOKEN.")
        else:
            raise Exception(f"GitHub API error {e.response.status_code}: {e.response.text}")
    except Exception as e:
        raise Exception(f"Request failed: {str(e)}")


@mcp.tool()
def get_repository_info(owner: str, repo: str) -> str:
    """
    Get detailed information about a GitHub repository.
    
    Retrieves repository metadata including stars, forks, description,
    language, license, open issues, and more.
    
    Args:
        owner: Repository owner (username or organization)
        repo: Repository name
        
    Returns:
        JSON string with repository information
        
    Example:
        owner="openai", repo="gpt-3"
    """
    try:
        data = make_github_request(f"repos/{owner}/{repo}")
        
        result = {
            "name": data["full_name"],
            "description": data.get("description", "No description"),
            "url": data["html_url"],
            "created_at": data["created_at"],
            "updated_at": data["updated_at"],
            "language": data.get("language", "Not specified"),
            "statistics": {
                "stars": data["stargazers_count"],
                "watchers": data["watchers_count"],
                "forks": data["forks_count"],
                "open_issues": data["open_issues_count"],
                "size_kb": data["size"]
            },
            "features": {
                "has_wiki": data["has_wiki"],
                "has_pages": data["has_pages"],
                "has_issues": data["has_issues"],
                "has_projects": data["has_projects"],
                "has_downloads": data["has_downloads"]
            },
            "license": data["license"]["name"] if data.get("license") else "No license",
            "default_branch": data["default_branch"],
            "topics": data.get("topics", []),
            "is_fork": data["fork"],
            "is_archived": data["archived"],
            "visibility": data["visibility"]
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def search_repositories(query: str, sort: str = "stars", limit: int = 10) -> str:
    """
    Search GitHub repositories by query.
    
    Find repositories matching keywords, language, topics, etc.
    
    Args:
        query: Search query (e.g., "machine learning language:python")
        sort: Sort by 'stars', 'forks', 'updated', or 'best-match' (default: stars)
        limit: Number of results to return (1-100, default: 10)
        
    Returns:
        JSON string with search results
        
    Example:
        query="fastapi", sort="stars", limit=5
    """
    try:
        limit = max(1, min(limit, 100))
        
        params = {
            "q": query,
            "sort": sort,
            "per_page": limit,
            "order": "desc"
        }
        
        data = make_github_request("search/repositories", params)
        
        repositories = []
        for repo in data["items"]:
            repositories.append({
                "name": repo["full_name"],
                "description": repo.get("description", "")[:200],
                "url": repo["html_url"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "language": repo.get("language", "Unknown"),
                "updated_at": repo["updated_at"],
                "topics": repo.get("topics", [])[:5]
            })
        
        result = {
            "total_count": data["total_count"],
            "showing": len(repositories),
            "repositories": repositories
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def get_repository_commits(owner: str, repo: str, limit: int = 10) -> str:
    """
    Get recent commits from a repository.
    
    Retrieves commit history with author, message, and timestamp.
    
    Args:
        owner: Repository owner
        repo: Repository name
        limit: Number of commits to return (1-100, default: 10)
        
    Returns:
        JSON string with commit history
        
    Example:
        owner="torvalds", repo="linux", limit=5
    """
    try:
        limit = max(1, min(limit, 100))
        
        params = {"per_page": limit}
        data = make_github_request(f"repos/{owner}/{repo}/commits", params)
        
        commits = []
        for commit in data:
            commits.append({
                "sha": commit["sha"][:7],
                "message": commit["commit"]["message"].split('\n')[0][:100],
                "author": commit["commit"]["author"]["name"],
                "date": commit["commit"]["author"]["date"],
                "url": commit["html_url"]
            })
        
        result = {
            "repository": f"{owner}/{repo}",
            "commit_count": len(commits),
            "commits": commits
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def get_repository_issues(owner: str, repo: str, state: str = "open", limit: int = 10) -> str:
    """
    Get issues from a repository.
    
    Retrieves open or closed issues with details.
    
    Args:
        owner: Repository owner
        repo: Repository name
        state: Issue state - 'open', 'closed', or 'all' (default: open)
        limit: Number of issues to return (1-100, default: 10)
        
    Returns:
        JSON string with issues
        
    Example:
        owner="facebook", repo="react", state="open", limit=5
    """
    try:
        limit = max(1, min(limit, 100))
        
        params = {
            "state": state,
            "per_page": limit,
            "sort": "updated",
            "direction": "desc"
        }
        
        data = make_github_request(f"repos/{owner}/{repo}/issues", params)
        
        issues = []
        for issue in data:
            # Skip pull requests (they appear in issues API)
            if "pull_request" in issue:
                continue
                
            issues.append({
                "number": issue["number"],
                "title": issue["title"],
                "state": issue["state"],
                "author": issue["user"]["login"],
                "created_at": issue["created_at"],
                "updated_at": issue["updated_at"],
                "comments": issue["comments"],
                "labels": [label["name"] for label in issue["labels"]],
                "url": issue["html_url"]
            })
        
        result = {
            "repository": f"{owner}/{repo}",
            "state_filter": state,
            "issue_count": len(issues),
            "issues": issues
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def get_file_content(owner: str, repo: str, path: str, branch: str = "main") -> str:
    """
    Get content of a file from a repository.
    
    Retrieves raw file content from any branch.
    
    Args:
        owner: Repository owner
        repo: Repository name
        path: File path (e.g., "src/main.py")
        branch: Branch name (default: main)
        
    Returns:
        JSON string with file content
        
    Example:
        owner="python", repo="cpython", path="README.rst"
    """
    try:
        params = {"ref": branch}
        data = make_github_request(f"repos/{owner}/{repo}/contents/{path}", params)
        
        # Decode base64 content
        if data.get("encoding") == "base64":
            content = base64.b64decode(data["content"]).decode('utf-8')
        else:
            content = data.get("content", "")
        
        result = {
            "repository": f"{owner}/{repo}",
            "path": data["path"],
            "name": data["name"],
            "size": data["size"],
            "type": data["type"],
            "url": data["html_url"],
            "content": content[:5000],  # Limit to first 5000 chars
            "truncated": len(content) > 5000
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def get_user_profile(username: str) -> str:
    """
    Get GitHub user profile information.
    
    Retrieves user bio, public repos, followers, and activity.
    
    Args:
        username: GitHub username
        
    Returns:
        JSON string with user profile
        
    Example:
        username="torvalds"
    """
    try:
        data = make_github_request(f"users/{username}")
        
        result = {
            "username": data["login"],
            "name": data.get("name", ""),
            "bio": data.get("bio", ""),
            "company": data.get("company", ""),
            "location": data.get("location", ""),
            "email": data.get("email", ""),
            "blog": data.get("blog", ""),
            "twitter": data.get("twitter_username", ""),
            "profile_url": data["html_url"],
            "avatar_url": data["avatar_url"],
            "statistics": {
                "public_repos": data["public_repos"],
                "public_gists": data["public_gists"],
                "followers": data["followers"],
                "following": data["following"]
            },
            "account": {
                "type": data["type"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"]
            }
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def get_trending_repositories(language: str = "", since: str = "daily") -> str:
    """
    Get trending repositories on GitHub.
    
    Note: Uses GitHub's trending page scraping (unofficial).
    
    Args:
        language: Filter by language (e.g., "python", "javascript") or "" for all
        since: Time period - "daily", "weekly", or "monthly" (default: daily)
        
    Returns:
        JSON string with trending repositories
        
    Example:
        language="python", since="weekly"
    """
    try:
        # This would typically use a trending API or web scraping
        # For now, using search with recent stars as proxy
        days_map = {"daily": 1, "weekly": 7, "monthly": 30}
        days = days_map.get(since, 1)
        
        date_filter = f"created:>={datetime.now().date().isoformat()}"
        query = f"stars:>100 {date_filter}"
        
        if language:
            query += f" language:{language}"
        
        params = {
            "q": query,
            "sort": "stars",
            "per_page": 10,
            "order": "desc"
        }
        
        data = make_github_request("search/repositories", params)
        
        repos = []
        for repo in data["items"][:10]:
            repos.append({
                "name": repo["full_name"],
                "description": repo.get("description", "")[:200],
                "url": repo["html_url"],
                "stars": repo["stargazers_count"],
                "language": repo.get("language", "Unknown"),
                "stars_today": "N/A"  # Would need additional API call
            })
        
        result = {
            "period": since,
            "language": language if language else "all",
            "repositories": repos
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def search_code(query: str, owner: str = "", repo: str = "", limit: int = 10) -> str:
    """
    Search code across GitHub repositories.
    
    Find code snippets matching your query.
    
    Args:
        query: Search query (e.g., "def main" or "import pandas")
        owner: Optional repository owner filter
        repo: Optional repository name filter (requires owner)
        limit: Number of results (1-100, default: 10)
        
    Returns:
        JSON string with code search results
        
    Example:
        query="async def", owner="fastapi", limit=5
    """
    try:
        limit = max(1, min(limit, 100))
        
        search_query = query
        if owner and repo:
            search_query = f"{query} repo:{owner}/{repo}"
        elif owner:
            search_query = f"{query} user:{owner}"
        
        params = {
            "q": search_query,
            "per_page": limit
        }
        
        data = make_github_request("search/code", params)
        
        results = []
        for item in data["items"]:
            results.append({
                "name": item["name"],
                "path": item["path"],
                "repository": item["repository"]["full_name"],
                "url": item["html_url"],
                "score": item["score"]
            })
        
        result = {
            "query": query,
            "total_count": data["total_count"],
            "showing": len(results),
            "results": results
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def server_info() -> str:
    """
    Get information about the GitHub Analyzer MCP Server.
    
    Returns server details including version, available tools,
    and usage information.
    
    Returns:
        JSON string with server information
    """
    info = {
        "server_name": "GitHub Analyzer MCP Server",
        "version": "1.0.0",
        "description": "Analyze GitHub repositories, search code, view issues, and get statistics",
        "api_provider": "GitHub REST API v3",
        "transport": "HTTP",
        "tools": [
            "get_repository_info",
            "search_repositories",
            "get_repository_commits",
            "get_repository_issues",
            "get_file_content",
            "get_user_profile",
            "get_trending_repositories",
            "search_code",
            "server_info"
        ],
        "features": [
            "Repository analysis and statistics",
            "Code search across repositories",
            "Issue and PR tracking",
            "Commit history viewing",
            "File content retrieval",
            "User profile information",
            "Trending repository discovery",
            "Advanced search capabilities"
        ],
        "rate_limits": {
            "without_token": "60 requests per hour",
            "with_token": "5000 requests per hour (recommended)"
        },
        "authentication": {
            "required": False,
            "recommended": True,
            "env_var": "GITHUB_TOKEN",
            "get_token": "https://github.com/settings/tokens"
        },
        "author": "GitHub MCP Developer",
        "documentation": "https://github.com/yourusername/github-mcp-server"
    }
    
    return json.dumps(info, indent=2)


if __name__ == "__main__":
    print("🐙 Starting GitHub Analyzer MCP Server...")
    print(f"📡 Transport: HTTP")
    print(f"🌐 Host: 0.0.0.0")
    print(f"🔌 Port: 8001")
    print(f"🔑 GitHub Token: {'✓ Set' if GITHUB_TOKEN else '✗ Not Set (60 req/hr limit)'}")
    print("\n📝 Available tools: 9")
    print("   • get_repository_info")
    print("   • search_repositories")
    print("   • get_repository_commits")
    print("   • get_repository_issues")
    print("   • get_file_content")
    print("   • get_user_profile")
    print("   • get_trending_repositories")
    print("   • search_code")
    print("   • server_info")
    print("\n🚀 Server ready! Access at http://localhost:8001\n")
    
    mcp.run(transport='http', host='0.0.0.0', port=8001)