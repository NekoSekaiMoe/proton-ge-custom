#!/usr/bin/env python3

import argparse
import subprocess
import shutil
import os
import sys
from pathlib import Path

def run(cmd, cwd=None, verbose=False):
    if verbose:
        print(f"[CMD] {' '.join(cmd)}", file=sys.stderr)
    subprocess.run(cmd, cwd=cwd, check=True)

def find_and_remove(pattern, root='.'):
    """Remove all files/dirs matching pattern under root."""
    for item in Path(root).rglob(pattern):
        if item.exists():
            if verbose_global:
                print(f"[RM] {item}", file=sys.stderr)
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

def main():
    global verbose_global
    parser = argparse.ArgumentParser(description="Bump glslang to the latest version.")
    parser.add_argument('--verbose', '-v', action='store_true', help="Enable verbose output")
    args = parser.parse_args()
    verbose_global = args.verbose

    repo_dir = Path("glslang")

    # Remove old glslang directory if exists
    if repo_dir.exists():
        if args.verbose:
            print(f"[RM] Removing {repo_dir}", file=sys.stderr)
        shutil.rmtree(repo_dir)

    # Clone glslang
    run(["git", "clone", "https://github.com/KhronosGroup/glslang", "--depth=1"], verbose=args.verbose)
    os.chdir(repo_dir)

    # Update external sources
    run([sys.executable, "update_glslang_sources.py"], verbose=args.verbose)

    # Remove .gitignore, .git, .github
    find_and_remove(".gitignore")
    find_and_remove(".git")
    find_and_remove(".github")

    os.chdir("..")

    # Git add & commit
    run(["git", "add", "."], verbose=args.verbose)
    run(["git", "commit", "-m", "Bump glslang to latest"], verbose=args.verbose)

    # Rebase and push
    run(["git", "pull", "--rebase"], verbose=args.verbose)
    run(["git", "push"], verbose=args.verbose)

if __name__ == "__main__":
    main()
