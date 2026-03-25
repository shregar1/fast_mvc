"""
`fastmvc config` — View and validate application configuration.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


def _load_env_file(env_path: Path) -> dict[str, str]:
    """Load environment variables from .env file."""
    env_vars: dict[str, str] = {}
    if not env_path.exists():
        return env_vars
    
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                env_vars[key] = value
    return env_vars


def _mask_sensitive_value(key: str, value: str) -> str:
    """Mask sensitive values like passwords and secrets."""
    sensitive_patterns = [
        "password", "secret", "key", "token", "auth", "credential",
        "api_key", "private", "salt", "jwt"
    ]
    
    key_lower = key.lower()
    for pattern in sensitive_patterns:
        if pattern in key_lower:
            if len(value) <= 8:
                return "***"
            return value[:4] + "***" + value[-4:]
    return value


def show_config(
    project_dir: Path,
    env: str | None = None,
    format: str = "table",
    show_secrets: bool = False,
    filter_key: str | None = None,
) -> int:
    """
    Display application configuration.
    
    Args:
        project_dir: Project root directory
        env: Environment name (dev, staging, prod)
        format: Output format (table, json, yaml)
        show_secrets: Show actual secret values instead of masking
        filter_key: Filter by key substring
    
    Returns:
        0 on success, 1 on error
    """
    env_file = project_dir / ".env"
    if not env_file.exists():
        env_example = project_dir / ".env.example"
        if env_example.exists():
            env_file = env_example
        else:
            print(f"No .env or .env.example file found in {project_dir}")
            return 1
    
    config = _load_env_file(env_file)
    
    # Apply filter
    if filter_key:
        config = {k: v for k, v in config.items() if filter_key.lower() in k.lower()}
    
    if format == "json":
        output = {k: (v if show_secrets else _mask_sensitive_value(k, v)) for k, v in config.items()}
        print(json.dumps(output, indent=2))
    elif format == "yaml":
        for key, value in sorted(config.items()):
            display_value = value if show_secrets else _mask_sensitive_value(key, value)
            print(f"{key}: {display_value}")
    else:  # table
        print(f"\nConfiguration from: {env_file}\n")
        print(f"{'Key':<40} {'Value':<50}")
        print("-" * 90)
        
        for key in sorted(config.keys()):
            value = config[key]
            display_value = value if show_secrets else _mask_sensitive_value(key, value)
            # Truncate long values
            if len(display_value) > 47:
                display_value = display_value[:44] + "..."
            print(f"{key:<40} {display_value:<50}")
        
        print(f"\nTotal: {len(config)} variables")
        if not show_secrets:
            print("Use --show-secrets to display actual values.")
        print()
    
    return 0


def validate_config(project_dir: Path) -> int:
    """
    Validate configuration and check for common issues.
    
    Returns:
        0 if valid, 1 if issues found
    """
    env_file = project_dir / ".env"
    env_example = project_dir / ".env.example"
    
    if not env_file.exists():
        print(f"✗ .env file not found: {env_file}")
        return 1
    
    issues = []
    warnings = []
    
    config = _load_env_file(env_file)
    
    # Check required variables
    required_vars = [
        "DATABASE_URL",
        ("DATABASE_HOST", "DATABASE_PORT", "DATABASE_NAME", "DATABASE_USER", "DATABASE_PASSWORD"),
    ]
    
    for req in required_vars:
        if isinstance(req, tuple):
            if not any(r in config and config[r] for r in req):
                issues.append(f"Missing one of: {', '.join(req)}")
        elif req not in config or not config[req]:
            issues.append(f"Missing required variable: {req}")
    
    # Check default/placeholder values
    defaults = [
        ("JWT_SECRET_KEY", "your-super-secret-jwt-key"),
        ("DATABASE_PASSWORD", "postgres123"),
        ("BCRYPT_SALT", "$2b$12$LQv3c1yqBWVHxkd0LHAkCO"),
    ]
    
    for var, default in defaults:
        if var in config and config[var] == default:
            warnings.append(f"{var} is using default value")
    
    # Check for .env.example sync
    if env_example.exists():
        example_config = _load_env_file(env_example)
        env_keys = set(config.keys())
        example_keys = set(example_config.keys())
        
        missing_in_env = example_keys - env_keys
        extra_in_env = env_keys - example_keys
        
        for key in missing_in_env:
            if not key.startswith("#"):
                warnings.append(f"{key} present in .env.example but missing in .env")
    
    # Print results
    print(f"\nConfiguration Validation: {env_file}\n")
    
    if issues:
        print("Errors:")
        for issue in issues:
            print(f"  ✗ {issue}")
    
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  ⚠ {warning}")
    
    if not issues and not warnings:
        print("✓ Configuration looks good!")
    
    print()
    
    return 1 if issues else 0


def diff_config(project_dir: Path) -> int:
    """
    Compare .env with .env.example and show differences.
    
    Returns:
        0 on success, 1 on error
    """
    env_file = project_dir / ".env"
    env_example = project_dir / ".env.example"
    
    if not env_file.exists():
        print(f"✗ .env file not found: {env_file}")
        return 1
    
    if not env_example.exists():
        print(f"✗ .env.example file not found: {env_example}")
        return 1
    
    env_config = _load_env_file(env_file)
    example_config = _load_env_file(env_example)
    
    env_keys = set(env_config.keys())
    example_keys = set(example_config.keys())
    
    only_in_env = sorted(env_keys - example_keys)
    only_in_example = sorted(example_keys - env_keys)
    different_values = []
    
    for key in sorted(env_keys & example_keys):
        if env_config[key] != example_config[key]:
            different_values.append((key, env_config[key], example_config[key]))
    
    print(f"\nConfiguration Diff: {env_file.name} vs {env_example.name}\n")
    
    if only_in_example:
        print(f"Missing in .env ({len(only_in_example)}):")
        for key in only_in_example:
            print(f"  + {key}={example_config[key][:50]}")
        print()
    
    if only_in_env:
        print(f"Extra in .env ({len(only_in_env)}):")
        for key in only_in_env:
            print(f"  - {key}={env_config[key][:50]}")
        print()
    
    if different_values:
        print(f"Different values ({len(different_values)}):")
        for key, env_val, ex_val in different_values:
            env_display = env_val[:40] + "..." if len(env_val) > 40 else env_val
            ex_display = ex_val[:40] + "..." if len(ex_val) > 40 else ex_val
            print(f"  ~ {key}")
            print(f"    .env:         {env_display}")
            print(f"    .env.example: {ex_display}")
        print()
    
    if not any([only_in_env, only_in_example, different_values]):
        print("✓ .env and .env.example are in sync!\n")
    
    return 0
