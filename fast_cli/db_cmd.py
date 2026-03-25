"""
`fastmvc db` — Database operations (seed, reset, drop, stats).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def _get_database_url(project_dir: Path) -> str | None:
    """Get database URL from environment or .env file."""
    # Try loading from .env
    env_file = project_dir / ".env"
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("DATABASE_URL="):
                    return line.split("=", 1)[1].strip().strip('"\'')
    
    # Build from individual env vars
    host = os.environ.get("DATABASE_HOST")
    if host:
        port = os.environ.get("DATABASE_PORT", "5432")
        name = os.environ.get("DATABASE_NAME", "postgres")
        user = os.environ.get("DATABASE_USER", "postgres")
        password = os.environ.get("DATABASE_PASSWORD", "")
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
    
    # Check environment directly
    return os.environ.get("DATABASE_URL")


def _run_sql(url: str, sql: str) -> tuple[bool, str]:
    """Execute SQL and return (success, output_or_error)."""
    try:
        from sqlalchemy import create_engine, text
        
        engine = create_engine(url, pool_pre_ping=True)
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            conn.commit()
            
            # Try to fetch results
            if result.returns_rows:
                rows = result.fetchall()
                return True, json.dumps([dict(row._mapping) for row in rows], indent=2, default=str)
            return True, "OK"
    except Exception as e:
        return False, str(e)


def db_seed(
    project_dir: Path,
    seeder: str | None = None,
    dry_run: bool = False,
) -> int:
    """
    Seed the database with initial data.
    
    Args:
        project_dir: Project root directory
        seeder: Specific seeder to run
        dry_run: Show what would be done without executing
    
    Returns:
        0 on success, 1 on error
    """
    url = _get_database_url(project_dir)
    if not url:
        print("✗ DATABASE_URL not configured")
        return 1
    
    print(f"\nSeeding database...\n")
    
    # Look for seeders
    seeders_dir = project_dir / "seeders"
    if not seeders_dir.exists():
        seeders_dir = project_dir / "seeds"
    
    if seeders_dir.exists():
        seed_files = sorted(seeders_dir.glob("*.py"))
        
        if seeder:
            seed_files = [f for f in seed_files if seeder in f.name]
        
        if not seed_files:
            print(f"No seeder files found in {seeders_dir}")
            return 0
        
        for seed_file in seed_files:
            if dry_run:
                print(f"  [DRY-RUN] Would run: {seed_file.name}")
                continue
            
            print(f"  Running: {seed_file.name}")
            try:
                # Run the seeder file
                result = subprocess.run(
                    [sys.executable, str(seed_file)],
                    cwd=project_dir,
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0:
                    print(f"    ✗ Failed: {result.stderr}")
                    return 1
                print(f"    ✓ Success")
            except Exception as e:
                print(f"    ✗ Error: {e}")
                return 1
    else:
        # Run SQL seed if available
        seed_sql = project_dir / "seed.sql"
        if seed_sql.exists():
            if dry_run:
                print(f"  [DRY-RUN] Would execute: {seed_sql}")
            else:
                print(f"  Executing: {seed_sql}")
                sql = seed_sql.read_text()
                success, output = _run_sql(url, sql)
                if success:
                    print(f"    ✓ Success")
                else:
                    print(f"    ✗ Failed: {output}")
                    return 1
        else:
            print("No seeders found. Create a seeders/ directory or seed.sql file.")
            return 0
    
    print("\n✓ Database seeded successfully\n")
    return 0


def db_reset(project_dir: Path, force: bool = False) -> int:
    """
    Reset database (drop all tables and recreate).
    
    Args:
        project_dir: Project root directory
        force: Skip confirmation prompt
    
    Returns:
        0 on success, 1 on error
    """
    url = _get_database_url(project_dir)
    if not url:
        print("✗ DATABASE_URL not configured")
        return 1
    
    if not force:
        print("\n⚠ WARNING: This will drop all tables and data!")
        confirm = input("Type 'RESET' to confirm: ")
        if confirm != "RESET":
            print("Aborted.")
            return 1
    
    print(f"\nResetting database...\n")
    
    # Run Alembic downgrade to base
    try:
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "downgrade", "base"],
            cwd=project_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0 and "No such revision" not in result.stderr:
            print(f"  Warning during downgrade: {result.stderr}")
    except Exception as e:
        print(f"  Warning: Could not run alembic downgrade: {e}")
    
    # Alternative: drop and recreate using SQLAlchemy
    try:
        from sqlalchemy import create_engine, MetaData
        from sqlalchemy.orm import sessionmaker
        
        engine = create_engine(url, pool_pre_ping=True)
        metadata = MetaData()
        metadata.reflect(bind=engine)
        
        # Drop all tables
        metadata.drop_all(bind=engine)
        print("  ✓ Dropped all tables")
        
        # Re-run migrations
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            cwd=project_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("  ✓ Ran migrations")
        else:
            print(f"  Warning: Migration issue: {result.stderr}")
        
    except Exception as e:
        print(f"  ✗ Error resetting database: {e}")
        return 1
    
    print("\n✓ Database reset successfully\n")
    return 0


def db_drop(project_dir: Path, force: bool = False) -> int:
    """
    Drop all database tables.
    
    Args:
        project_dir: Project root directory
        force: Skip confirmation prompt
    
    Returns:
        0 on success, 1 on error
    """
    url = _get_database_url(project_dir)
    if not url:
        print("✗ DATABASE_URL not configured")
        return 1
    
    if not force:
        print("\n⚠ WARNING: This will drop ALL tables and data!")
        confirm = input("Type 'DROP' to confirm: ")
        if confirm != "DROP":
            print("Aborted.")
            return 1
    
    print(f"\nDropping all tables...\n")
    
    try:
        from sqlalchemy import create_engine, MetaData
        
        engine = create_engine(url, pool_pre_ping=True)
        metadata = MetaData()
        metadata.reflect(bind=engine)
        
        metadata.drop_all(bind=engine)
        print("  ✓ Dropped all tables")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return 1
    
    print("\n✓ All tables dropped\n")
    return 0


def db_stats(project_dir: Path) -> int:
    """
    Show database statistics.
    
    Returns:
        0 on success, 1 on error
    """
    url = _get_database_url(project_dir)
    if not url:
        print("✗ DATABASE_URL not configured")
        return 1
    
    print(f"\nDatabase Statistics\n")
    
    try:
        from sqlalchemy import create_engine, text
        
        engine = create_engine(url, pool_pre_ping=True)
        
        # Get database info
        with engine.connect() as conn:
            # PostgreSQL specific
            if "postgresql" in url:
                result = conn.execute(text("SELECT current_database(), version()"))
                row = result.fetchone()
                if row:
                    print(f"Database: {row[0]}")
                    print(f"Version: {row[1][:50]}...")
                print()
                
                # Table statistics
                result = conn.execute(text("""
                    SELECT schemaname, relname, n_live_tup
                    FROM pg_stat_user_tables
                    ORDER BY n_live_tup DESC
                """))
                
                rows = result.fetchall()
                if rows:
                    print("Table Statistics:")
                    print(f"{'Schema':<20} {'Table':<30} {'Rows':>10}")
                    print("-" * 62)
                    for row in rows:
                        print(f"{row[0]:<20} {row[1]:<30} {row[2]:>10}")
                    print()
                
                # Database size
                result = conn.execute(text("""
                    SELECT pg_size_pretty(pg_database_size(current_database()))
                """))
                size = result.fetchone()
                if size:
                    print(f"Database Size: {size[0]}")
                
            # MySQL specific
            elif "mysql" in url:
                result = conn.execute(text("SELECT DATABASE(), VERSION()"))
                row = result.fetchone()
                if row:
                    print(f"Database: {row[0]}")
                    print(f"Version: {row[1]}")
                print()
                
                # Table statistics
                result = conn.execute(text("""
                    SELECT table_name, table_rows
                    FROM information_schema.tables
                    WHERE table_schema = DATABASE()
                    ORDER BY table_rows DESC
                """))
                
                rows = result.fetchall()
                if rows:
                    print("Table Statistics:")
                    print(f"{'Table':<40} {'Rows':>10}")
                    print("-" * 52)
                    for row in rows:
                        print(f"{row[0]:<40} {row[1] or 0:>10}")
                    print()
            
            else:
                # Generic - show table names
                from sqlalchemy import inspect
                inspector = inspect(engine)
                tables = inspector.get_table_names()
                print(f"Tables ({len(tables)}):")
                for table in sorted(tables):
                    print(f"  - {table}")
        
        print()
        return 0
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return 1
