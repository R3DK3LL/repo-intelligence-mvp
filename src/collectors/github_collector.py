"""
GitHub Data Collector - Extracts repository data for analysis
"""

import os
from github import Github
from typing import Dict, List, Optional
import requests
from urllib.parse import urlparse


class GitHubCollector:
    def __init__(self, token: Optional[str] = None):
        """Initialize with GitHub token (optional but recommended for rate limits)"""
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.github = Github(self.token) if self.token else Github()

    def extract_repo_data(self, repo_url: str) -> Dict:
        """
        Extract all necessary data from a GitHub repository

        Args:
            repo_url: GitHub repository URL

        Returns:
            dict: Repository data including commits, PRs, contributors, etc.
        """
        repo_path = self._parse_repo_url(repo_url)
        if not repo_path:
            raise ValueError(f"Invalid GitHub URL: {repo_url}")

        try:
            repo = self.github.get_repo(repo_path)

            return {
                "basic_info": self._get_basic_info(repo),
                "commits": self._get_commit_data(repo),
                "pull_requests": self._get_pr_data(repo),
                "contributors": self._get_contributor_data(repo),
                "branches": self._get_branch_data(repo),
                "issues": self._get_issue_data(repo),
                "repository_stats": self._get_repo_stats(repo),
            }

        except Exception as e:
            raise Exception(f"Failed to collect data from {repo_url}: {str(e)}")

    def _parse_repo_url(self, url: str) -> Optional[str]:
        """Extract owner/repo from GitHub URL"""
        try:
            parsed = urlparse(url)
            if "github.com" not in parsed.netloc:
                return None

            path_parts = parsed.path.strip("/").split("/")
            if len(path_parts) >= 2:
                return f"{path_parts[0]}/{path_parts[1]}"
            return None
        except:
            return None

    def _get_basic_info(self, repo) -> Dict:
        """Get basic repository information"""
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "created_at": repo.created_at.isoformat() if repo.created_at else None,
            "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
            "language": repo.language,
            "size": repo.size,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "open_issues": repo.open_issues_count,
        }

    def _get_commit_data(self, repo, limit: int = 500) -> List[Dict]:
        """Get commit history data"""
        commits = []
        try:
            for commit in repo.get_commits()[:limit]:
                commits.append(
                    {
                        "sha": commit.sha,
                        "author": (
                            commit.commit.author.name
                            if commit.commit.author
                            else "Unknown"
                        ),
                        "author_login": commit.author.login if commit.author else None,
                        "date": (
                            commit.commit.author.date.isoformat()
                            if commit.commit.author.date
                            else None
                        ),
                        "message": commit.commit.message,
                        "files_changed": len(commit.files) if commit.files else 0,
                        "additions": commit.stats.additions if commit.stats else 0,
                        "deletions": commit.stats.deletions if commit.stats else 0,
                    }
                )
        except Exception as e:
            print(f"Warning: Could not fetch all commits: {e}")

        return commits

    def _get_pr_data(self, repo, limit: int = 200) -> List[Dict]:
        """Get pull request data"""
        prs = []
        try:
            for pr in repo.get_pulls(state="all")[:limit]:
                prs.append(
                    {
                        "number": pr.number,
                        "title": pr.title,
                        "state": pr.state,
                        "created_at": (
                            pr.created_at.isoformat() if pr.created_at else None
                        ),
                        "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
                        "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
                        "author": pr.user.login if pr.user else None,
                        "reviews": len(list(pr.get_reviews())),
                        "comments": pr.comments,
                        "additions": pr.additions,
                        "deletions": pr.deletions,
                        "changed_files": pr.changed_files,
                    }
                )
        except Exception as e:
            print(f"Warning: Could not fetch all PRs: {e}")

        return prs

    def _get_contributor_data(self, repo) -> List[Dict]:
        """Get contributor information"""
        contributors = []
        try:
            for contributor in repo.get_contributors():
                contributors.append(
                    {
                        "login": contributor.login,
                        "contributions": contributor.contributions,
                        "type": contributor.type,
                    }
                )
        except Exception as e:
            print(f"Warning: Could not fetch contributors: {e}")

        return contributors

    def _get_branch_data(self, repo) -> List[Dict]:
        """Get branch information"""
        branches = []
        try:
            for branch in repo.get_branches():
                branches.append(
                    {
                        "name": branch.name,
                        "protected": branch.protected,
                        "commit_sha": branch.commit.sha,
                    }
                )
        except Exception as e:
            print(f"Warning: Could not fetch branches: {e}")

        return branches

    def _get_issue_data(self, repo, limit: int = 100) -> List[Dict]:
        """Get issues data"""
        issues = []
        try:
            for issue in repo.get_issues(state="all")[:limit]:
                if not issue.pull_request:  # Exclude PRs from issues
                    issues.append(
                        {
                            "number": issue.number,
                            "title": issue.title,
                            "state": issue.state,
                            "created_at": (
                                issue.created_at.isoformat()
                                if issue.created_at
                                else None
                            ),
                            "closed_at": (
                                issue.closed_at.isoformat() if issue.closed_at else None
                            ),
                            "labels": [label.name for label in issue.labels],
                            "comments": issue.comments,
                        }
                    )
        except Exception as e:
            print(f"Warning: Could not fetch issues: {e}")

        return issues

    def _get_repo_stats(self, repo) -> Dict:
        """Get additional repository statistics"""
        try:
            languages = repo.get_languages()
            return {
                "languages": languages,
                "has_wiki": repo.has_wiki,
                "has_pages": repo.has_pages,
                "has_projects": repo.has_projects,
                "archived": repo.archived,
                "disabled": repo.disabled,
                "default_branch": repo.default_branch,
            }
        except Exception as e:
            print(f"Warning: Could not fetch repo stats: {e}")
            return {}
