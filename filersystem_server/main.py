#!/usr/bin/env python3

import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("filesystem")

@mcp.tool()
async def read_file(path: str) -> str:
    """Read the complete contents of a file.
    
    Args:
        path: Path to the file to read
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def write_file(path: str, content: str) -> str:
    """Write content to a file.
    
    Args:
        path: Path to the file to write
        content: Content to write to the file
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def list_directory(path: str) -> str:
    """List all files and directories in a path.
    
    Args:
        path: Directory path to list
    """
    try:
        entries = []
        for entry in sorted(os.listdir(path)):
            entry_path = os.path.join(path, entry)
            prefix = "[DIR]" if os.path.isdir(entry_path) else "[FILE]"
            entries.append(f"{prefix} {entry}")
        return "\n".join(entries) if entries else "Directory is empty"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool() 
async def search_files(path: str, pattern: str) -> str:
    """Search for files matching a pattern.
    
    Args:
        path: Directory to search in
        pattern: Filename pattern to match (supports * wildcards)
    """
    try:
        import fnmatch
        matches = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if fnmatch.fnmatch(file, pattern):
                    matches.append(os.path.join(root, file))
        return "\n".join(matches) if matches else f"No files found matching '{pattern}'"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport='stdio')