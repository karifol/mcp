import importlib
import pkgutil
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP(stateless_http=True, json_response=True)

# Auto-load all tools from the tools directory
tools_dir = Path(__file__).parent / "tools"
if tools_dir.exists():
    for _, module_name, _ in pkgutil.iter_modules([str(tools_dir)]):
        # Import the module to register tools defined with @mcp.tool()
        importlib.import_module(f"app.tools.{module_name}")

app = mcp.http_app()