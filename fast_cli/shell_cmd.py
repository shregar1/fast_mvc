"""
`fastmvc shell` — Interactive shell with application context.
"""

from __future__ import annotations

import code
import sys
from pathlib import Path
from typing import Any


def _get_banner() -> str:
    """Return the shell banner."""
    return """
╔══════════════════════════════════════════════════════════════╗
║                   FastMVC Interactive Shell                  ║
╚══════════════════════════════════════════════════════════════╝

Available variables:
  app       - FastAPI application instance
  db        - Database session/dependency (if available)
  settings  - Application settings (if available)
  models    - SQLAlchemy models module

Type help() for Python help, exit() or Ctrl+D to exit.
"""


def start_shell(
    project_dir: Path,
    shell_type: str = "ipython",
    no_banner: bool = False,
) -> int:
    """
    Start an interactive shell with the application context loaded.
    
    Args:
        project_dir: Project root directory
        shell_type: Type of shell to start (ipython, bpython, ptpython, python)
        no_banner: Suppress the welcome banner
    
    Returns:
        0 on success, 1 on error
    """
    # Add project directory to path
    sys.path.insert(0, str(project_dir))
    
    # Prepare namespace
    namespace: dict[str, Any] = {
        "__name__": "__fastmvc_shell__",
        "__doc__": None,
    }
    
    # Try to load the application
    app_path = project_dir / "app.py"
    if app_path.exists():
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("app", app_path)
            if spec and spec.loader:
                app_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(app_module)
                
                if hasattr(app_module, "app"):
                    namespace["app"] = app_module.app
                if hasattr(app_module, "get_db"):
                    namespace["db"] = app_module.get_db
        except Exception as e:
            print(f"Warning: Could not load app.py: {e}")
    
    # Try to load models
    models_path = project_dir / "models"
    if models_path.exists():
        try:
            import models
            namespace["models"] = models
            
            # Add common models directly to namespace
            for attr_name in dir(models):
                if not attr_name.startswith("_"):
                    namespace[attr_name] = getattr(models, attr_name)
        except Exception as e:
            print(f"Warning: Could not load models: {e}")
    
    # Try to load settings/config
    try:
        config_path = project_dir / "config"
        if config_path.exists():
            sys.path.insert(0, str(config_path))
            try:
                from configurations import default
                if hasattr(default, "Settings"):
                    namespace["Settings"] = default.Settings
                    namespace["settings"] = default.Settings()
            except ImportError:
                pass
    except Exception:
        pass
    
    # Try IPython first
    if shell_type in ("ipython", "auto"):
        try:
            from IPython import start_ipython
            from IPython.terminal.interactiveshell import TerminalInteractiveShell
            
            if not no_banner:
                print(_get_banner())
            
            # Start IPython with our namespace
            ipython_shell = TerminalInteractiveShell.instance(
                user_ns=namespace,
                banner1="" if no_banner else None,
                banner2="",
            )
            ipython_shell.mainloop()
            return 0
        except ImportError:
            if shell_type == "ipython":
                print("IPython not installed. Falling back to standard Python shell.")
                shell_type = "python"
    
    # Try bpython
    if shell_type in ("bpython", "auto"):
        try:
            import bpython
            if not no_banner:
                print(_get_banner())
            bpython.embed(locals_=namespace)
            return 0
        except ImportError:
            if shell_type == "bpython":
                print("bpython not installed. Falling back to standard Python shell.")
                shell_type = "python"
    
    # Try ptpython
    if shell_type in ("ptpython", "auto"):
        try:
            from ptpython.repl import embed
            if not no_banner:
                print(_get_banner())
            embed(globals=namespace, locals=namespace)
            return 0
        except ImportError:
            if shell_type == "ptpython":
                print("ptpython not installed. Falling back to standard Python shell.")
                shell_type = "python"
    
    # Standard Python shell
    if not no_banner:
        print(_get_banner())
    
    # Enable tab completion if available
    try:
        import readline
        import rlcompleter
        readline.parse_and_bind("tab: complete")
    except ImportError:
        pass
    
    code.interact(
        banner="",
        local=namespace,
    )
    return 0
