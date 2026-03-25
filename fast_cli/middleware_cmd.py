"""
`fastmvc middleware` — List, enable, and disable middleware.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any


# Known FastMVC middlewares with descriptions
KNOWN_MIDDLEWARES: dict[str, dict[str, Any]] = {
    "RequestContextMiddleware": {
        "description": "Request tracking with unique URN generation",
        "import_path": "fastmiddleware.request_context.RequestContextMiddleware",
        "category": "core",
    },
    "TimingMiddleware": {
        "description": "Response timing headers (X-Response-Time)",
        "import_path": "fastmiddleware.timing.TimingMiddleware",
        "category": "observability",
    },
    "LoggingMiddleware": {
        "description": "Structured request/response logging",
        "import_path": "fastmiddleware.logging.LoggingMiddleware",
        "category": "observability",
    },
    "RateLimitMiddleware": {
        "description": "Rate limiting with sliding window",
        "import_path": "fastmiddleware.rate_limit.RateLimitMiddleware",
        "category": "security",
    },
    "SecurityHeadersMiddleware": {
        "description": "Security headers (CSP, HSTS, XSS protection)",
        "import_path": "fastmiddleware.security.SecurityHeadersMiddleware",
        "category": "security",
    },
    "CORSMiddleware": {
        "description": "Cross-Origin Resource Sharing",
        "import_path": "fastmiddleware.cors.CORSMiddleware",
        "category": "security",
    },
    "AuthenticationMiddleware": {
        "description": "JWT authentication validation",
        "import_path": "fastmiddleware.auth.AuthenticationMiddleware",
        "category": "auth",
    },
    "AuthorizationMiddleware": {
        "description": "Role-based access control",
        "import_path": "fastmiddleware.auth.AuthorizationMiddleware",
        "category": "auth",
    },
    "IdempotencyMiddleware": {
        "description": "Idempotency key handling",
        "import_path": "fastmiddleware.idempotency.IdempotencyMiddleware",
        "category": "reliability",
    },
    "CachingMiddleware": {
        "description": "Response caching with Redis",
        "import_path": "fastmiddleware.cache.CachingMiddleware",
        "category": "performance",
    },
    "CompressionMiddleware": {
        "description": "Gzip/Brotli response compression",
        "import_path": "fastmiddleware.compression.CompressionMiddleware",
        "category": "performance",
    },
}


def _find_app_file(project_dir: Path) -> Path | None:
    """Find the main app.py file."""
    candidates = [
        project_dir / "app.py",
        project_dir / "main.py",
        project_dir / "application.py",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _extract_middlewares(app_file: Path) -> list[dict[str, Any]]:
    """Extract middleware configuration from app.py."""
    content = app_file.read_text()
    
    middlewares = []
    
    # Look for add_middleware calls
    pattern = r'add_middleware\s*\(\s*([^\)]+)\)'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        middleware_text = match.group(1)
        
        # Extract class name
        class_match = re.search(r'(\w+Middleware)', middleware_text)
        if class_match:
            name = class_match.group(1)
            
            # Check if it's commented out
            line_start = content[:match.start()].rfind('\n')
            is_commented = content[line_start:match.start()].strip().startswith('#')
            
            # Extract parameters
            params = {}
            param_matches = re.finditer(r'(\w+)\s*=\s*([^,\)]+)', middleware_text)
            for pm in param_matches:
                params[pm.group(1)] = pm.group(2).strip()
            
            middlewares.append({
                "name": name,
                "enabled": not is_commented,
                "params": params,
            })
    
    return middlewares


def list_middlewares(
    project_dir: Path,
    show_all: bool = False,
    category: str | None = None,
) -> int:
    """
    List all middlewares and their status.
    
    Returns:
        0 on success, 1 on error
    """
    app_file = _find_app_file(project_dir)
    
    if not app_file:
        print("✗ Could not find app.py")
        return 1
    
    configured = _extract_middlewares(app_file)
    configured_names = {m["name"] for m in configured}
    
    print(f"\nMiddleware Status ({app_file.name})\n")
    
    if show_all:
        # Show all known middlewares
        items = KNOWN_MIDDLEWARES.items()
        if category:
            items = [(k, v) for k, v in items if v.get("category") == category]
        
        for name, info in sorted(items, key=lambda x: x[1].get("category", "")):
            status = "✓" if name in configured_names else "✗"
            enabled_info = ""
            for cm in configured:
                if cm["name"] == name:
                    enabled_info = " (enabled)" if cm["enabled"] else " (disabled)"
                    break
            
            print(f"{status} {name:<35} {info.get('category', 'unknown'):<15} {info.get('description', '')[:40]}{enabled_info}")
    else:
        # Show only configured middlewares
        if not configured:
            print("No middlewares found in app.py")
        else:
            print(f"{'Status':<10} {'Middleware':<35} {'Category':<15}")
            print("-" * 60)
            for mw in configured:
                status = "✓ enabled" if mw["enabled"] else "✗ disabled"
                known = KNOWN_MIDDLEWARES.get(mw["name"], {})
                cat = known.get("category", "custom")
                print(f"{status:<10} {mw['name']:<35} {cat:<15}")
                
                if mw["params"]:
                    for k, v in mw["params"].items():
                        print(f"           └─ {k}={v}")
    
    print()
    print(f"Total configured: {len([m for m in configured if m['enabled']])} enabled, {len([m for m in configured if not m['enabled']])} disabled")
    print(f"Use --show-all to see available middlewares")
    print()
    
    return 0


def add_middleware(
    project_dir: Path,
    middleware_name: str,
    params: dict[str, str] | None = None,
) -> int:
    """
    Add a middleware to the application.
    
    Returns:
        0 on success, 1 on error
    """
    app_file = _find_app_file(project_dir)
    if not app_file:
        print("✗ Could not find app.py")
        return 1
    
    content = app_file.read_text()
    
    # Check if already exists
    if middleware_name in content:
        print(f"⚠ {middleware_name} appears to already be in app.py")
        return 0
    
    # Get middleware info
    info = KNOWN_MIDDLEWARES.get(middleware_name, {})
    import_path = info.get("import_path", f"fastmiddleware.{middleware_name.lower().replace('middleware', '')}.{middleware_name}")
    
    # Build import statement
    module_path = ".".join(import_path.split(".")[:-1])
    import_stmt = f"from {module_path} import {middleware_name}\n"
    
    # Add import if not present
    if import_stmt.strip() not in content:
        # Find a good place to add import
        lines = content.split("\n")
        import_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("from ") or line.startswith("import "):
                import_idx = i + 1
        lines.insert(import_idx, import_stmt.rstrip())
        content = "\n".join(lines)
    
    # Build add_middleware call
    param_str = ", ".join([f"{k}={v}" for k, v in (params or {}).items()])
    middleware_call = f"app.add_middleware({middleware_name}{', ' + param_str if param_str else ''})\n"
    
    # Find place to add middleware (after other middlewares or in setup section)
    if "add_middleware" in content:
        # Add after last add_middleware
        content = re.sub(
            r'(add_middleware\([^\)]+\)\n)',
            r'\1' + middleware_call,
            content
        )
    else:
        # Add before app.include_router or at end
        content = re.sub(
            r'(app\.include_router|if __name__)',
            middleware_call + r'\1',
            content
        )
    
    app_file.write_text(content)
    print(f"✓ Added {middleware_name} to {app_file.name}")
    print(f"  Import: {import_stmt.strip()}")
    print(f"  Call: {middleware_call.strip()}")
    print()
    
    return 0


def remove_middleware(project_dir: Path, middleware_name: str) -> int:
    """
    Remove or comment out a middleware.
    
    Returns:
        0 on success, 1 on error
    """
    app_file = _find_app_file(project_dir)
    if not app_file:
        print("✗ Could not find app.py")
        return 1
    
    content = app_file.read_text()
    
    # Find and comment out the middleware
    pattern = rf'^\s*(app\.add_middleware\s*\(\s*{middleware_name}[^\)]*\))'
    
    if not re.search(pattern, content, re.MULTILINE):
        print(f"⚠ {middleware_name} not found in {app_file.name}")
        return 0
    
    new_content = re.sub(
        pattern,
        r'# \1  # Disabled by fastmvc',
        content,
        flags=re.MULTILINE
    )
    
    app_file.write_text(new_content)
    print(f"✓ Disabled {middleware_name} in {app_file.name}")
    print()
    
    return 0


def reorder_middlewares(project_dir: Path, order: list[str]) -> int:
    """
    Reorder middlewares in the application.
    
    Middlewares in FastAPI run in reverse order of addition (last added runs first).
    
    Returns:
        0 on success, 1 on error
    """
    app_file = _find_app_file(project_dir)
    if not app_file:
        print("✗ Could not find app.py")
        return 1
    
    content = app_file.read_text()
    lines = content.split("\n")
    
    # Extract all middleware lines
    middleware_lines = []
    other_lines = []
    
    for line in lines:
        if "add_middleware" in line and not line.strip().startswith("#"):
            middleware_lines.append(line)
        else:
            other_lines.append(line)
    
    if len(middleware_lines) < 2:
        print("⚠ Not enough middlewares to reorder")
        return 0
    
    # Build reorder map
    order_map = {name: idx for idx, name in enumerate(order)}
    
    # Sort middleware lines by order
    def sort_key(line):
        for name in order:
            if name in line:
                return order_map.get(name, 999)
        return 999
    
    sorted_middlewares = sorted(middleware_lines, key=sort_key, reverse=True)
    
    # Rebuild content
    result = []
    mw_idx = 0
    for line in other_lines:
        if "add_middleware" in line and not line.strip().startswith("#"):
            result.append(sorted_middlewares[mw_idx])
            mw_idx += 1
        else:
            result.append(line)
    
    app_file.write_text("\n".join(result))
    print("✓ Reordered middlewares")
    print()
    print("New order (execution order, first runs last):")
    for line in sorted_middlewares:
        match = re.search(r'add_middleware\s*\(\s*(\w+)', line)
        if match:
            print(f"  - {match.group(1)}")
    print()
    
    return 0
