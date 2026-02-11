from mcp.server.fastmcp import FastMCP

# Import ONLY pure calculators
from tools.sip_calculator import sip_calculator
from tools.retirement_calculator import retirement_corpus_calculator
from tools.emi_calculator import emi_calculator
from tools.emergency_fund_calculator import emergency_fund_calculator
from tools.asset_allocation_tool import asset_allocation

mcp = FastMCP("finance-calculators")

# Register deterministic calculators only
mcp.add_tool(sip_calculator)
mcp.add_tool(retirement_corpus_calculator)
mcp.add_tool(emi_calculator)
mcp.add_tool(emergency_fund_calculator)
mcp.add_tool(asset_allocation)

if __name__ == "__main__":
    mcp.run()


    