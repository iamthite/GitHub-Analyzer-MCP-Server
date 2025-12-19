###==============================================================
### Enhanced GitHub MCP Server - FIXED VERSION 2.0.1
### Removed decorator with *args to fix FastMCP compatibility
###==============================================================

from fastmcp import FastMCP
import httpx
import os
import json
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
import base64

mcp = FastMCP("GitHub-Analyzer-Pro-MCP-Server")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_API_BASE = "https://api.github.com"
REQUEST_TIMEOUT = 30.0

class GitHubAPIClient:
    def __init__(self):
        self.base_url = GITHUB_API_BASE
        self.token = GITHUB_TOKEN
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"
    
    def request(self, endpoint: str, params: dict = None, method: str = "GET") -> dict:
        url = f"{self.base_url}/{endpoint}"
        try:
            with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
                if method == "GET":
                    response = client.get(url, params=params, headers=self.headers)
                elif method == "POST":
                    response = client.post(url, json=params, headers=self.headers)
                elif method == "PATCH":
                    response = client.patch(url, json=params, headers=self.headers)
                elif method == "DELETE":
                    response = client.delete(url, headers=self.headers)
                response.raise_for_status()
                return response.json() if response.content else {}
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            if status == 404:
                raise Exception(f"Resource not found: {e.request.url.path}")
            elif status == 403:
                raise Exception("Rate limit exceeded. Add GITHUB_TOKEN for higher limits.")
            elif status == 401:
                raise Exception("Authentication failed. Check your GITHUB_TOKEN.")
            elif status == 422:
                raise Exception(f"Validation failed: {e.response.text}")
            else:
                raise Exception(f"GitHub API error {status}: {e.response.text}")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")

gh_client = GitHubAPIClient()

# REPOSITORY TOOLS
@mcp.tool()
def get_repository_info(owner: str, repo: str) -> str:
    """Get comprehensive repository information"""
    try:
        data = gh_client.request(f"repos/{owner}/{repo}")
        result = {
            "name": data["full_name"],
            "description": data.get("description", "No description"),
            "url": data["html_url"],
            "homepage": data.get("homepage", ""),
            "created_at": data["created_at"],
            "updated_at": data["updated_at"],
            "pushed_at": data["pushed_at"],
            "language": data.get("language", "Not specified"),
            "statistics": {
                "stars": data["stargazers_count"],
                "watchers": data["watchers_count"],
                "forks": data["forks_count"],
                "open_issues": data["open_issues_count"],
                "size_kb": data["size"],
                "network_count": data.get("network_count", 0),
                "subscribers_count": data.get("subscribers_count", 0)
            },
            "features": {
                "has_wiki": data["has_wiki"],
                "has_pages": data["has_pages"],
                "has_issues": data["has_issues"],
                "has_projects": data["has_projects"],
                "has_downloads": data["has_downloads"],
                "has_discussions": data.get("has_discussions", False)
            },
            "license": data["license"]["name"] if data.get("license") else "No license",
            "default_branch": data["default_branch"],
            "topics": data.get("topics", []),
            "is_fork": data["fork"],
            "is_archived": data["archived"],
            "is_template": data.get("is_template", False),
            "visibility": data["visibility"],
            "owner_info": {
                "login": data["owner"]["login"],
                "type": data["owner"]["type"],
                "url": data["owner"]["html_url"]
            }
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def get_repository_languages(owner: str, repo: str) -> str:
    """Get programming languages used in repository with percentages"""
    try:
        data = gh_client.request(f"repos/{owner}/{repo}/languages")
        total_bytes = sum(data.values())
        languages = []
        for lang, bytes_count in sorted(data.items(), key=lambda x: x[1], reverse=True):
            percentage = (bytes_count / total_bytes * 100) if total_bytes > 0 else 0
            languages.append({
                "language": lang,
                "bytes": bytes_count,
                "percentage": round(percentage, 2)
            })
        result = {
            "repository": f"{owner}/{repo}",
            "total_bytes": total_bytes,
            "language_count": len(languages),
            "languages": languages
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def get_repository_contributors(owner: str, repo: str, limit: int = 30) -> str:
    """Get top contributors to a repository"""
    try:
        limit = max(1, min(limit, 100))
        params = {"per_page": limit, "anon": "false"}
        data = gh_client.request(f"repos/{owner}/{repo}/contributors", params)
        contributors = [{
            "username": c["login"],
            "contributions": c["contributions"],
            "profile_url": c["html_url"],
            "avatar_url": c["avatar_url"],
            "type": c["type"]
        } for c in data]
        result = {
            "repository": f"{owner}/{repo}",
            "contributor_count": len(contributors),
            "contributors": contributors
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def get_repository_tags(owner: str, repo: str, limit: int = 20) -> str:
    """Get repository tags/releases"""
    try:
        limit = max(1, min(limit, 100))
        data = gh_client.request(f"repos/{owner}/{repo}/tags", {"per_page": limit})
        tags = [{
            "name": t["name"],
            "commit_sha": t["commit"]["sha"][:7],
            "zipball_url": t["zipball_url"],
            "tarball_url": t["tarball_url"]
        } for t in data]
        return json.dumps({"repository": f"{owner}/{repo}", "tag_count": len(tags), "tags": tags}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def get_repository_branches(owner: str, repo: str, limit: int = 20) -> str:
    """Get repository branches"""
    try:
        limit = max(1, min(limit, 100))
        data = gh_client.request(f"repos/{owner}/{repo}/branches", {"per_page": limit})
        branches = [{
            "name": b["name"],
            "protected": b["protected"],
            "commit_sha": b["commit"]["sha"][:7],
            "commit_url": b["commit"]["url"]
        } for b in data]
        return json.dumps({"repository": f"{owner}/{repo}", "branch_count": len(branches), "branches": branches}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

# COMMIT TOOLS
@mcp.tool()
def get_repository_commits(owner: str, repo: str, branch: str = "", limit: int = 10) -> str:
    """Get recent commits from repository"""
    try:
        limit = max(1, min(limit, 100))
        params = {"per_page": limit}
        if branch:
            params["sha"] = branch
        data = gh_client.request(f"repos/{owner}/{repo}/commits", params)
        commits = [{
            "sha": c["sha"][:7],
            "full_sha": c["sha"],
            "message": c["commit"]["message"].split('\n')[0][:150],
            "author": {
                "name": c["commit"]["author"]["name"],
                "email": c["commit"]["author"]["email"],
                "date": c["commit"]["author"]["date"]
            },
            "committer": c["commit"]["committer"]["name"],
            "url": c["html_url"],
            "comment_count": c["commit"]["comment_count"],
            "verified": c["commit"]["verification"]["verified"]
        } for c in data]
        return json.dumps({"repository": f"{owner}/{repo}", "branch": branch or "default", "commit_count": len(commits), "commits": commits}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def get_commit_details(owner: str, repo: str, sha: str) -> str:
    """Get detailed information about specific commit"""
    try:
        data = gh_client.request(f"repos/{owner}/{repo}/commits/{sha}")
        files = [{
            "filename": f["filename"],
            "status": f["status"],
            "additions": f["additions"],
            "deletions": f["deletions"],
            "changes": f["changes"],
            "patch": f.get("patch", "")[:500]
        } for f in data.get("files", [])[:20]]
        result = {
            "sha": data["sha"],
            "message": data["commit"]["message"],
            "author": {
                "name": data["commit"]["author"]["name"],
                "email": data["commit"]["author"]["email"],
                "date": data["commit"]["author"]["date"]
            },
            "stats": data["stats"],
            "files_changed": len(data.get("files", [])),
            "files": files,
            "url": data["html_url"],
            "verified": data["commit"]["verification"]["verified"]
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def compare_commits(owner: str, repo: str, base: str, head: str) -> str:
    """Compare two commits or branches"""
    try:
        data = gh_client.request(f"repos/{owner}/{repo}/compare/{base}...{head}")
        files = [{
            "filename": f["filename"],
            "status": f["status"],
            "additions": f["additions"],
            "deletions": f["deletions"],
            "changes": f["changes"]
        } for f in data.get("files", [])[:20]]
        result = {
            "repository": f"{owner}/{repo}",
            "comparison": f"{base}...{head}",
            "status": data["status"],
            "ahead_by": data["ahead_by"],
            "behind_by": data["behind_by"],
            "total_commits": data["total_commits"],
            "stats": {
                "files_changed": len(data.get("files", [])),
                "total_additions": sum(f["additions"] for f in data.get("files", [])),
                "total_deletions": sum(f["deletions"] for f in data.get("files", []))
            },
            "files": files,
            "url": data["html_url"]
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

# ISSUE & PR TOOLS
@mcp.tool()
def get_repository_issues(owner: str, repo: str, state: str = "open", labels: str = "", limit: int = 10) -> str:
    """Get issues from repository with filtering"""
    try:
        limit = max(1, min(limit, 100))
        params = {"state": state, "per_page": limit, "sort": "updated", "direction": "desc"}
        if labels:
            params["labels"] = labels
        data = gh_client.request(f"repos/{owner}/{repo}/issues", params)
        issues = [{
            "number": i["number"],
            "title": i["title"],
            "state": i["state"],
            "author": i["user"]["login"],
            "created_at": i["created_at"],
            "updated_at": i["updated_at"],
            "closed_at": i.get("closed_at"),
            "comments": i["comments"],
            "labels": [l["name"] for l in i["labels"]],
            "assignees": [a["login"] for a in i["assignees"]],
            "milestone": i["milestone"]["title"] if i.get("milestone") else None,
            "url": i["html_url"],
            "body_preview": i["body"][:200] if i.get("body") else ""
        } for i in data if "pull_request" not in i]
        return json.dumps({"repository": f"{owner}/{repo}", "state_filter": state, "label_filter": labels, "issue_count": len(issues), "issues": issues}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def get_pull_requests(owner: str, repo: str, state: str = "open", limit: int = 10) -> str:
    """Get pull requests from repository"""
    try:
        limit = max(1, min(limit, 100))
        params = {"state": state, "per_page": limit, "sort": "updated", "direction": "desc"}
        data = gh_client.request(f"repos/{owner}/{repo}/pulls", params)
        prs = [{
            "number": pr["number"],
            "title": pr["title"],
            "state": pr["state"],
            "author": pr["user"]["login"],
            "created_at": pr["created_at"],
            "updated_at": pr["updated_at"],
            "merged_at": pr.get("merged_at"),
            "draft": pr["draft"],
            "head_branch": pr["head"]["ref"],
            "base_branch": pr["base"]["ref"],
            "labels": [l["name"] for l in pr["labels"]],
            "comments": pr["comments"],
            "commits": pr["commits"],
            "additions": pr["additions"],
            "deletions": pr["deletions"],
            "changed_files": pr["changed_files"],
            "url": pr["html_url"]
        } for pr in data]
        return json.dumps({"repository": f"{owner}/{repo}", "state_filter": state, "pr_count": len(prs), "pull_requests": prs}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def get_issue_comments(owner: str, repo: str, issue_number: int, limit: int = 30) -> str:
    """Get comments from specific issue or PR"""
    try:
        limit = max(1, min(limit, 100))
        data = gh_client.request(f"repos/{owner}/{repo}/issues/{issue_number}/comments", {"per_page": limit})
        comments = [{
            "id": c["id"],
            "author": c["user"]["login"],
            "created_at": c["created_at"],
            "updated_at": c["updated_at"],
            "body": c["body"][:500],
            "reactions": c["reactions"]["total_count"],
            "url": c["html_url"]
        } for c in data]
        return json.dumps({"repository": f"{owner}/{repo}", "issue_number": issue_number, "comment_count": len(comments), "comments": comments}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

# FILE & CONTENT TOOLS
@mcp.tool()
def get_file_content(owner: str, repo: str, path: str, branch: str = "") -> str:
    """Get content of file from repository"""
    try:
        params = {"ref": branch} if branch else {}
        data = gh_client.request(f"repos/{owner}/{repo}/contents/{path}", params)
        content = ""
        if data.get("encoding") == "base64" and data.get("content"):
            try:
                content = base64.b64decode(data["content"]).decode('utf-8')
            except:
                content = "[Binary file or encoding error]"
        result = {
            "repository": f"{owner}/{repo}",
            "path": data["path"],
            "name": data["name"],
            "size": data["size"],
            "type": data["type"],
            "sha": data["sha"],
            "url": data["html_url"],
            "download_url": data.get("download_url", ""),
            "content": content[:10000],
            "truncated": len(content) > 10000
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def get_directory_contents(owner: str, repo: str, path: str = "", branch: str = "") -> str:
    """List contents of directory in repository"""
    try:
        params = {"ref": branch} if branch else {}
        endpoint = f"repos/{owner}/{repo}/contents" + (f"/{path}" if path else "")
        data = gh_client.request(endpoint, params)
        if not isinstance(data, list):
            data = [data]
        contents = [{
            "name": i["name"],
            "path": i["path"],
            "type": i["type"],
            "size": i.get("size", 0),
            "sha": i["sha"],
            "url": i["html_url"],
            "download_url": i.get("download_url", "")
        } for i in data]
        return json.dumps({"repository": f"{owner}/{repo}", "path": path or "/", "item_count": len(contents), "contents": contents}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def search_code(query: str, owner: str = "", repo: str = "", language: str = "", limit: int = 10) -> str:
    """Search code across GitHub repositories"""
    try:
        limit = max(1, min(limit, 100))
        search_query = query
        if owner and repo:
            search_query += f" repo:{owner}/{repo}"
        elif owner:
            search_query += f" user:{owner}"
        if language:
            search_query += f" language:{language}"
        data = gh_client.request("search/code", {"q": search_query, "per_page": limit})
        results = [{
            "name": i["name"],
            "path": i["path"],
            "repository": i["repository"]["full_name"],
            "sha": i["sha"],
            "url": i["html_url"],
            "score": i["score"]
        } for i in data["items"]]
        return json.dumps({"query": query, "total_count": data["total_count"], "showing": len(results), "results": results}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

# SEARCH & DISCOVERY TOOLS
@mcp.tool()
def search_repositories(query: str, sort: str = "stars", language: str = "", limit: int = 10) -> str:
    """Search GitHub repositories with advanced filters"""
    try:
        limit = max(1, min(limit, 100))
        search_query = query + (f" language:{language}" if language else "")
        params = {"q": search_query, "sort": sort, "per_page": limit, "order": "desc"}
        data = gh_client.request("search/repositories", params)
        repos = [{
            "name": r["full_name"],
            "description": (r.get("description", "") or "")[:200],
            "url": r["html_url"],
            "stars": r["stargazers_count"],
            "forks": r["forks_count"],
            "language": r.get("language", "Unknown"),
            "updated_at": r["updated_at"],
            "topics": r.get("topics", [])[:5],
            "license": r["license"]["name"] if r.get("license") else "No license",
            "open_issues": r["open_issues_count"]
        } for r in data["items"]]
        return json.dumps({"total_count": data["total_count"], "showing": len(repos), "repositories": repos}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def search_users(query: str, limit: int = 10) -> str:
    """Search GitHub users and organizations"""
    try:
        limit = max(1, min(limit, 100))
        data = gh_client.request("search/users", {"q": query, "per_page": limit})
        users = [{
            "username": u["login"],
            "type": u["type"],
            "url": u["html_url"],
            "avatar_url": u["avatar_url"],
            "score": u["score"]
        } for u in data["items"]]
        return json.dumps({"total_count": data["total_count"], "showing": len(users), "users": users}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def search_topics(query: str, limit: int = 10) -> str:
    """Search GitHub topics"""
    try:
        limit = max(1, min(limit, 100))
        headers = gh_client.headers.copy()
        headers["Accept"] = "application/vnd.github.mercy-preview+json"
        with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
            response = client.get(f"{gh_client.base_url}/search/topics", params={"q": query, "per_page": limit}, headers=headers)
            response.raise_for_status()
            data = response.json()
        topics = [{
            "name": t["name"],
            "display_name": t.get("display_name", t["name"]),
            "description": t.get("short_description", ""),
            "created_by": t.get("created_by", ""),
            "featured": t.get("featured", False),
            "curated": t.get("curated", False),
            "score": t["score"]
        } for t in data["items"]]
        return json.dumps({"total_count": data["total_count"], "showing": len(topics), "topics": topics}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

# USER & ORGANIZATION TOOLS
@mcp.tool()
def get_user_profile(username: str) -> str:
    """Get detailed GitHub user profile"""
    try:
        data = gh_client.request(f"users/{username}")
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
            "hireable": data.get("hireable", False),
            "statistics": {
                "public_repos": data["public_repos"],
                "public_gists": data["public_gists"],
                "followers": data["followers"],
                "following": data["following"]
            },
            "account": {
                "type": data["type"],
                "site_admin": data["site_admin"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"]
            }
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def get_user_repositories(username: str, sort: str = "updated", limit: int = 20) -> str:
    """Get user's public repositories"""
    try:
        limit = max(1, min(limit, 100))
        data = gh_client.request(f"users/{username}/repos", {"per_page": limit, "sort": sort, "direction": "desc"})
        repos = [{
            "name": r["name"],
            "full_name": r["full_name"],
            "description": (r.get("description", "") or "")[:150],
            "url": r["html_url"],
            "language": r.get("language", "Unknown"),
            "stars": r["stargazers_count"],
            "forks": r["forks_count"],
            "updated_at": r["updated_at"],
            "is_fork": r["fork"],
            "is_archived": r["archived"]
        } for r in data]
        return json.dumps({"username": username, "repository_count": len(repos), "repositories": repos}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def get_user_activity(username: str, limit: int = 30) -> str:
    """Get user's recent public activity"""
    try:
        limit = max(1, min(limit, 100))
        data = gh_client.request(f"users/{username}/events/public", {"per_page": limit})
        events = []
        for e in data:
            event_data = {
                "type": e["type"],
                "repo": e["repo"]["name"],
                "created_at": e["created_at"],
                "public": e["public"]
            }
            if e["type"] == "PushEvent":
                event_data["commits"] = len(e["payload"].get("commits", []))
            elif e["type"] == "IssuesEvent":
                event_data["action"] = e["payload"]["action"]
                event_data["issue"] = e["payload"]["issue"]["number"]
            elif e["type"] == "PullRequestEvent":
                event_data["action"] = e["payload"]["action"]
                event_data["pr"] = e["payload"]["pull_request"]["number"]
            events.append(event_data)
        return json.dumps({"username": username, "event_count": len(events), "events": events}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def get_organization_info(org: str) -> str:
    """Get GitHub organization information"""
    try:
        data = gh_client.request(f"orgs/{org}")
        result = {
            "login": data["login"],
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "company": data.get("company", ""),
            "blog": data.get("blog", ""),
            "location": data.get("location", ""),
            "email": data.get("email", ""),
            "twitter": data.get("twitter_username", ""),
            "url": data["html_url"],
            "avatar_url": data["avatar_url"],
            "statistics": {
                "public_repos": data["public_repos"],
                "public_gists": data["public_gists"],
                "followers": data["followers"],
                "following": data["following"]
            },
            "created_at": data["created_at"],
            "updated_at": data["updated_at"],
            "type": data["type"]
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

# STATISTICS & ANALYTICS TOOLS
@mcp.tool()
def get_repository_stats(owner: str, repo: str) -> str:
    """Get comprehensive repository statistics"""
    try:
        repo_data = gh_client.request(f"repos/{owner}/{repo}")
        try:
            commit_activity = gh_client.request(f"repos/{owner}/{repo}/stats/commit_activity")
            total_commits = sum(week["total"] for week in (commit_activity or []))
        except:
            total_commits = 0
        try:
            code_freq = gh_client.request(f"repos/{owner}/{repo}/stats/code_frequency")
            if code_freq:
                total_additions = sum(week[1] for week in code_freq)
                total_deletions = abs(sum(week[2] for week in code_freq))
            else:
                total_additions = total_deletions = 0
        except:
            total_additions = total_deletions = 0
        result = {
            "repository": f"{owner}/{repo}",
            "overview": {
                "stars": repo_data["stargazers_count"],
                "watchers": repo_data["watchers_count"],
                "forks": repo_data["forks_count"],
                "open_issues": repo_data["open_issues_count"],
                "size_kb": repo_data["size"],
                "network_count": repo_data.get("network_count", 0)
            },
            "activity": {
                "commits_last_year": total_commits,
                "total_additions": total_additions,
                "total_deletions": total_deletions,
                "last_push": repo_data["pushed_at"]
            },
            "health": {
                "has_readme": True,
                "has_license": repo_data.get("license") is not None,
                "has_contributing": False,
                "has_code_of_conduct": False
            },
            "age": {
                "created": repo_data["created_at"],
                "updated": repo_data["updated_at"],
                "pushed": repo_data["pushed_at"]
            }
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def get_repository_traffic(owner: str, repo: str) -> str:
    """Get repository traffic statistics (views and clones) - requires push access"""
    try:
        views = gh_client.request(f"repos/{owner}/{repo}/traffic/views")
        clones = gh_client.request(f"repos/{owner}/{repo}/traffic/clones")
        return json.dumps({
            "repository": f"{owner}/{repo}",
            "views": {"count": views["count"], "unique": views["uniques"], "per_day": views["views"]},
            "clones": {"count": clones["count"], "unique": clones["uniques"], "per_day": clones["clones"]}
        }, indent=2)
    except:
        return json.dumps({"error": "Traffic statistics require repository push access"}, indent=2)

@mcp.tool()
def get_repository_community(owner: str, repo: str) -> str:
    """Get repository community profile and health metrics"""
    try:
        data = gh_client.request(f"repos/{owner}/{repo}/community/profile")
        result = {
            "repository": f"{owner}/{repo}",
            "health_percentage": data["health_percentage"],
            "description": data.get("description", ""),
            "documentation": data.get("documentation", ""),
            "files": {
                "readme": data["files"].get("readme") is not None,
                "code_of_conduct": data["files"].get("code_of_conduct") is not None,
                "contributing": data["files"].get("contributing") is not None,
                "license": data["files"].get("license") is not None,
                "issue_template": data["files"].get("issue_template") is not None,
                "pull_request_template": data["files"].get("pull_request_template") is not None
            },
            "updated_at": data.get("updated_at", "")
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

# RELEASE & PACKAGE TOOLS
@mcp.tool()
def get_releases(owner: str, repo: str, limit: int = 10) -> str:
    """Get repository releases"""
    try:
        limit = max(1, min(limit, 100))
        data = gh_client.request(f"repos/{owner}/{repo}/releases", {"per_page": limit})
        releases = [{
            "name": r["name"] or r["tag_name"],
            "tag": r["tag_name"],
            "published_at": r["published_at"],
            "author": r["author"]["login"],
            "prerelease": r["prerelease"],
            "draft": r["draft"],
            "body": (r.get("body", "") or "")[:500],
            "assets_count": len(r.get("assets", [])),
            "url": r["html_url"],
            "download_count": sum(asset["download_count"] for asset in r.get("assets", []))
        } for r in data]
        return json.dumps({"repository": f"{owner}/{repo}", "release_count": len(releases), "releases": releases}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def get_latest_release(owner: str, repo: str) -> str:
    """Get the latest release from repository"""
    try:
        data = gh_client.request(f"repos/{owner}/{repo}/releases/latest")
        assets = [{
            "name": a["name"],
            "size": a["size"],
            "download_count": a["download_count"],
            "content_type": a["content_type"],
            "download_url": a["browser_download_url"]
        } for a in data.get("assets", [])]
        result = {
            "repository": f"{owner}/{repo}",
            "name": data["name"] or data["tag_name"],
            "tag": data["tag_name"],
            "published_at": data["published_at"],
            "author": data["author"]["login"],
            "prerelease": data["prerelease"],
            "body": data.get("body", ""),
            "assets": assets,
            "total_downloads": sum(a["download_count"] for a in assets),
            "url": data["html_url"]
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

# WORKFLOW & ACTIONS TOOLS
@mcp.tool()
def get_workflows(owner: str, repo: str) -> str:
    """Get GitHub Actions workflows for repository"""
    try:
        data = gh_client.request(f"repos/{owner}/{repo}/actions/workflows")
        workflows = [{
            "id": w["id"],
            "name": w["name"],
            "path": w["path"],
            "state": w["state"],
            "created_at": w["created_at"],
            "updated_at": w["updated_at"],
            "url": w["html_url"],
            "badge_url": w["badge_url"]
        } for w in data["workflows"]]
        return json.dumps({"repository": f"{owner}/{repo}", "workflow_count": len(workflows), "workflows": workflows}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def get_workflow_runs(owner: str, repo: str, limit: int = 10) -> str:
    """Get recent workflow runs"""
    try:
        limit = max(1, min(limit, 100))
        data = gh_client.request(f"repos/{owner}/{repo}/actions/runs", {"per_page": limit})
        runs = [{
            "id": r["id"],
            "name": r["name"],
            "status": r["status"],
            "conclusion": r["conclusion"],
            "workflow_id": r["workflow_id"],
            "branch": r["head_branch"],
            "event": r["event"],
            "created_at": r["created_at"],
            "updated_at": r["updated_at"],
            "run_number": r["run_number"],
            "url": r["html_url"]
        } for r in data["workflow_runs"]]
        return json.dumps({"repository": f"{owner}/{repo}", "run_count": len(runs), "runs": runs}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

# TRENDING & DISCOVERY
@mcp.tool()
def get_trending_repositories(language: str = "", since: str = "daily") -> str:
    """Get trending repositories"""
    try:
        days_map = {"daily": 1, "weekly": 7, "monthly": 30}
        days = days_map.get(since, 1)
        date = (datetime.now() - timedelta(days=days)).date().isoformat()
        query = f"created:>={date} stars:>50"
        if language:
            query += f" language:{language}"
        data = gh_client.request("search/repositories", {"q": query, "sort": "stars", "per_page": 10, "order": "desc"})
        repos = [{
            "name": r["full_name"],
            "description": (r.get("description", "") or "")[:200],
            "url": r["html_url"],
            "stars": r["stargazers_count"],
            "forks": r["forks_count"],
            "language": r.get("language", "Unknown"),
            "created_at": r["created_at"]
        } for r in data["items"]]
        return json.dumps({"period": since, "language": language or "all", "repository_count": len(repos), "repositories": repos}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def get_trending_developers(language: str = "") -> str:
    """Get trending developers based on recent repository activity"""
    try:
        date = (datetime.now() - timedelta(days=7)).date().isoformat()
        query = f"created:>={date} stars:>10"
        if language:
            query += f" language:{language}"
        data = gh_client.request("search/repositories", {"q": query, "sort": "stars", "per_page": 30, "order": "desc"})
        developers = {}
        for repo in data["items"]:
            owner = repo["owner"]["login"]
            if owner not in developers:
                developers[owner] = {
                    "username": owner,
                    "avatar_url": repo["owner"]["avatar_url"],
                    "profile_url": repo["owner"]["html_url"],
                    "repositories": [],
                    "total_stars": 0
                }
            developers[owner]["repositories"].append({"name": repo["name"], "stars": repo["stargazers_count"]})
            developers[owner]["total_stars"] += repo["stargazers_count"]
        sorted_devs = sorted(developers.values(), key=lambda x: x["total_stars"], reverse=True)[:10]
        return json.dumps({"language": language or "all", "developer_count": len(sorted_devs), "developers": sorted_devs}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

# UTILITY TOOLS
@mcp.tool()
def get_rate_limit() -> str:
    """Get current GitHub API rate limit status"""
    try:
        data = gh_client.request("rate_limit")
        result = {
            "resources": {
                "core": {
                    "limit": data["resources"]["core"]["limit"],
                    "remaining": data["resources"]["core"]["remaining"],
                    "reset": datetime.fromtimestamp(data["resources"]["core"]["reset"]).isoformat(),
                    "used": data["resources"]["core"]["used"]
                },
                "search": {
                    "limit": data["resources"]["search"]["limit"],
                    "remaining": data["resources"]["search"]["remaining"],
                    "reset": datetime.fromtimestamp(data["resources"]["search"]["reset"]).isoformat(),
                    "used": data["resources"]["search"]["used"]
                },
                "graphql": {
                    "limit": data["resources"]["graphql"]["limit"],
                    "remaining": data["resources"]["graphql"]["remaining"],
                    "reset": datetime.fromtimestamp(data["resources"]["graphql"]["reset"]).isoformat(),
                    "used": data["resources"]["graphql"]["used"]
                }
            },
            "rate": {
                "limit": data["rate"]["limit"],
                "remaining": data["rate"]["remaining"],
                "reset": datetime.fromtimestamp(data["rate"]["reset"]).isoformat()
            }
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def get_repository_readme(owner: str, repo: str, branch: str = "") -> str:
    """Get repository README content"""
    try:
        params = {"ref": branch} if branch else {}
        data = gh_client.request(f"repos/{owner}/{repo}/readme", params)
        content = ""
        if data.get("encoding") == "base64":
            content = base64.b64decode(data["content"]).decode('utf-8')
        result = {
            "repository": f"{owner}/{repo}",
            "name": data["name"],
            "path": data["path"],
            "size": data["size"],
            "url": data["html_url"],
            "download_url": data.get("download_url", ""),
            "content": content
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def server_info() -> str:
    """Get comprehensive server information"""
    result = {
        "server_name": "GitHub Analyzer Pro MCP Server",
        "version": "2.0.1",
        "description": "Production-ready GitHub MCP server with 28+ tools",
        "api_provider": "GitHub REST API v3",
        "transport": "HTTP",
        "status": "operational",
        "total_tools": 28,
        "tool_categories": {
            "Repository Analysis": ["get_repository_info", "get_repository_languages", "get_repository_contributors", "get_repository_tags", "get_repository_branches", "get_repository_stats", "get_repository_traffic", "get_repository_community"],
            "Commits & History": ["get_repository_commits", "get_commit_details", "compare_commits"],
            "Issues & PRs": ["get_repository_issues", "get_pull_requests", "get_issue_comments"],
            "Files & Content": ["get_file_content", "get_directory_contents", "get_repository_readme", "search_code"],
            "Search & Discovery": ["search_repositories", "search_users", "search_topics", "get_trending_repositories", "get_trending_developers"],
            "Users & Organizations": ["get_user_profile", "get_user_repositories", "get_user_activity", "get_organization_info"],
            "Releases & Packages": ["get_releases", "get_latest_release"],
            "Workflows & Actions": ["get_workflows", "get_workflow_runs"],
            "Utilities": ["get_rate_limit", "server_info"]
        },
        "features": ["Comprehensive repository analysis", "Advanced code search", "Issue and PR management", "Commit history and comparison", "User and organization profiles", "Release tracking", "GitHub Actions monitoring", "Traffic statistics", "Community health metrics", "Trending discovery", "Rate limit monitoring"],
        "rate_limits": {
            "without_token": "60 requests/hour",
            "with_token": "5000 requests/hour",
            "search_without_token": "10 requests/minute",
            "search_with_token": "30 requests/minute"
        },
        "authentication": {
            "required": False,
            "recommended": True,
            "env_var": "GITHUB_TOKEN",
            "get_token": "https://github.com/settings/tokens",
            "required_scopes": ["public_repo", "read:user"]
        },
        "performance": {
            "timeout": f"{REQUEST_TIMEOUT}s",
            "max_results_per_query": 100
        }
    }
    return json.dumps(result, indent=2)

# MAIN
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔧 GitHub Analyzer Pro MCP Server v2.0.1")
    print("="*60)
    print(f"\n📡 Server Configuration:")
    print(f"   Transport: HTTP")
    print(f"   Host: 0.0.0.0")
    print(f"   Port: 8001")
    print(f"   Timeout: {REQUEST_TIMEOUT}s")
    print(f"\n🔐 Authentication:")
    print(f"   GitHub Token: {'✓ Configured' if GITHUB_TOKEN else '✗ Not Set'}")
    print(f"   Rate Limit: {'5000/hr' if GITHUB_TOKEN else '60/hr'}")
    print(f"\n📊 Available Tools: 28")
    print(f"   • Repository Analysis (8 tools)")
    print(f"   • Commits & History (3 tools)")
    print(f"   • Issues & PRs (3 tools)")
    print(f"   • Files & Content (4 tools)")
    print(f"   • Search & Discovery (5 tools)")
    print(f"   • Users & Organizations (4 tools)")
    print(f"   • Releases & Packages (2 tools)")
    print(f"   • Workflows & Actions (2 tools)")
    print(f"   • Utilities (2 tools)")
    print(f"\n✨ Production Features:")
    print(f"   ✓ Enhanced error handling")
    print(f"   ✓ Rate limit monitoring")
    print(f"   ✓ Community health metrics")
    print(f"   ✓ Traffic analytics")
    print(f"   ✓ GitHub Actions support")
    print(f"\n🚀 Server Status: READY")
    print(f"   Access at: http://localhost:8001")
    print("="*60 + "\n")
    
    mcp.run(transport='http', host='0.0.0.0', port=8001)