#!/usr/bin/env python3
"""
Grocery Store Analytics MCP Server

This MCP server provides tools to query and analyze grocery store data from PostgreSQL.
"""

import asyncio
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

# Database connection parameters
DB_PARAMS = {
    'dbname': 'grocery_analytics',
    'user': 'arghya.mukherjee',
    'password': '',
    'host': 'localhost',
    'port': '5432'
}

# Initialize MCP server
server = Server("grocery-analytics")

def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(**DB_PARAMS, cursor_factory=RealDictCursor)

def format_currency(amount):
    """Format amount as Indian Rupees"""
    if amount is None:
        return "₹0.00"
    return f"₹{float(amount):,.2f}"

def execute_query(query, params=None):
    """Execute a query and return results"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        raise Exception(f"Database query failed: {str(e)}")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available MCP tools for grocery analytics"""
    return [
        types.Tool(
            name="get_sales_summary",
            description="Get overall sales summary including revenue, transactions, and customer metrics",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        types.Tool(
            name="get_top_products",
            description="Get top selling products by revenue or quantity",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Number of products to return (default: 10)",
                        "default": 10
                    },
                    "order_by": {
                        "type": "string",
                        "description": "Order by 'revenue' or 'quantity'",
                        "enum": ["revenue", "quantity"],
                        "default": "revenue"
                    }
                },
                "required": []
            },
        ),
        types.Tool(
            name="get_category_performance",
            description="Get sales performance by product category",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        types.Tool(
            name="get_customer_insights",
            description="Get customer segmentation and behavior insights",
            inputSchema={
                "type": "object",
                "properties": {
                    "segment": {
                        "type": "string",
                        "description": "Filter by customer segment: Regular, Premium, Occasional, New",
                        "enum": ["Regular", "Premium", "Occasional", "New", "all"],
                        "default": "all"
                    }
                },
                "required": []
            },
        ),
        types.Tool(
            name="get_store_performance",
            description="Get performance metrics for all stores or specific store",
            inputSchema={
                "type": "object",
                "properties": {
                    "store_id": {
                        "type": "string",
                        "description": "Specific store ID (e.g., STR_001) or 'all' for all stores",
                        "default": "all"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of stores to return",
                        "default": 10
                    }
                },
                "required": []
            },
        ),
        types.Tool(
            name="get_seasonal_analysis",
            description="Analyze sales performance by season (Winter, Summer, Monsoon, Spring)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        types.Tool(
            name="get_daily_sales_trend",
            description="Get daily sales trend for a date range",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date (YYYY-MM-DD format)",
                        "default": "2022-01-01"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date (YYYY-MM-DD format)",
                        "default": "2023-12-31"
                    }
                },
                "required": []
            },
        ),
        types.Tool(
            name="get_payment_method_analysis",
            description="Analyze payment method preferences and trends",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        types.Tool(
            name="get_hourly_traffic_pattern",
            description="Get hourly traffic patterns and peak shopping times",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        ),
        types.Tool(
            name="execute_custom_query",
            description="Execute a custom SQL query on the grocery database (for advanced analysis)",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL query to execute (SELECT statements only)"
                    }
                },
                "required": ["query"]
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests"""

    try:
        if name == "get_sales_summary":
            query = """
                SELECT
                    COUNT(*) as total_transactions,
                    SUM(total_amount) as total_revenue,
                    AVG(total_amount) as avg_transaction_value,
                    SUM(quantity) as total_items_sold,
                    COUNT(DISTINCT customer_id) as unique_customers,
                    COUNT(DISTINCT product_id) as unique_products,
                    MIN(timestamp) as start_date,
                    MAX(timestamp) as end_date
                FROM transactions
            """
            results = execute_query(query)
            data = results[0] if results else {}

            summary = f"""# Sales Summary

**Period**: {data.get('start_date')} to {data.get('end_date')}

## Key Metrics
- **Total Revenue**: {format_currency(data.get('total_revenue'))}
- **Total Transactions**: {data.get('total_transactions'):,}
- **Average Transaction Value**: {format_currency(data.get('avg_transaction_value'))}
- **Total Items Sold**: {data.get('total_items_sold'):,}
- **Unique Customers**: {data.get('unique_customers'):,}
- **Unique Products**: {data.get('unique_products')}
"""
            return [types.TextContent(type="text", text=summary)]

        elif name == "get_top_products":
            limit = arguments.get("limit", 10) if arguments else 10
            order_by = arguments.get("order_by", "revenue") if arguments else "revenue"

            order_column = "total_revenue" if order_by == "revenue" else "total_units_sold"

            query = f"""
                SELECT
                    product_name,
                    category,
                    brand,
                    transaction_count,
                    total_units_sold,
                    total_revenue,
                    avg_unit_price,
                    avg_discount
                FROM top_products
                ORDER BY {order_column} DESC
                LIMIT %s
            """
            results = execute_query(query, (limit,))

            output = f"# Top {limit} Products (by {order_by})\n\n"
            for idx, row in enumerate(results, 1):
                output += f"""
## {idx}. {row['product_name']}
- **Category**: {row['category']}
- **Brand**: {row['brand']}
- **Revenue**: {format_currency(row['total_revenue'])}
- **Units Sold**: {row['total_units_sold']:,}
- **Transactions**: {row['transaction_count']:,}
- **Avg Price**: {format_currency(row['avg_unit_price'])}
- **Avg Discount**: {row['avg_discount']:.1f}%
"""
            return [types.TextContent(type="text", text=output)]

        elif name == "get_category_performance":
            query = """
                SELECT
                    category,
                    transaction_count,
                    total_revenue,
                    avg_transaction_value,
                    total_units_sold,
                    revenue_percentage
                FROM category_performance
                ORDER BY total_revenue DESC
            """
            results = execute_query(query)

            output = "# Category Performance\n\n"
            for idx, row in enumerate(results, 1):
                output += f"""
## {idx}. {row['category']}
- **Revenue**: {format_currency(row['total_revenue'])} ({row['revenue_percentage']}%)
- **Transactions**: {row['transaction_count']:,}
- **Avg Transaction Value**: {format_currency(row['avg_transaction_value'])}
- **Units Sold**: {row['total_units_sold']:,}
"""
            return [types.TextContent(type="text", text=output)]

        elif name == "get_customer_insights":
            segment = arguments.get("segment", "all") if arguments else "all"

            if segment == "all":
                query = """
                    SELECT
                        customer_type,
                        COUNT(*) as customer_count,
                        SUM(visit_count) as total_visits,
                        SUM(lifetime_value) as total_revenue,
                        AVG(lifetime_value) as avg_lifetime_value,
                        AVG(visit_count) as avg_visits,
                        AVG(avg_transaction_value) as avg_transaction_value
                    FROM customer_insights
                    GROUP BY customer_type
                    ORDER BY total_revenue DESC
                """
            else:
                query = """
                    SELECT
                        customer_type,
                        COUNT(*) as customer_count,
                        SUM(visit_count) as total_visits,
                        SUM(lifetime_value) as total_revenue,
                        AVG(lifetime_value) as avg_lifetime_value,
                        AVG(visit_count) as avg_visits,
                        AVG(avg_transaction_value) as avg_transaction_value
                    FROM customer_insights
                    WHERE customer_type = %s
                    GROUP BY customer_type
                """
                results = execute_query(query, (segment,))

            if segment == "all":
                results = execute_query(query)

            output = f"# Customer Insights{' - ' + segment if segment != 'all' else ''}\n\n"
            for row in results:
                output += f"""
## {row['customer_type']} Customers
- **Count**: {row['customer_count']:,}
- **Total Revenue**: {format_currency(row['total_revenue'])}
- **Avg Lifetime Value**: {format_currency(row['avg_lifetime_value'])}
- **Total Visits**: {row['total_visits']:,}
- **Avg Visits per Customer**: {row['avg_visits']:.2f}
- **Avg Transaction Value**: {format_currency(row['avg_transaction_value'])}
"""
            return [types.TextContent(type="text", text=output)]

        elif name == "get_store_performance":
            store_id = arguments.get("store_id", "all") if arguments else "all"
            limit = arguments.get("limit", 10) if arguments else 10

            if store_id == "all":
                query = """
                    SELECT
                        store_id,
                        store_region,
                        store_type,
                        transaction_count,
                        total_revenue,
                        avg_transaction_value,
                        unique_customers
                    FROM store_performance
                    ORDER BY total_revenue DESC
                    LIMIT %s
                """
                results = execute_query(query, (limit,))
            else:
                query = """
                    SELECT
                        store_id,
                        store_region,
                        store_type,
                        transaction_count,
                        total_revenue,
                        avg_transaction_value,
                        unique_customers
                    FROM store_performance
                    WHERE store_id = %s
                """
                results = execute_query(query, (store_id,))

            output = f"# Store Performance{' - ' + store_id if store_id != 'all' else ''}\n\n"
            for idx, row in enumerate(results, 1):
                output += f"""
## {idx}. {row['store_id']} ({row['store_type']} - {row['store_region']})
- **Revenue**: {format_currency(row['total_revenue'])}
- **Transactions**: {row['transaction_count']:,}
- **Avg Transaction Value**: {format_currency(row['avg_transaction_value'])}
- **Unique Customers**: {row['unique_customers']:,}
"""
            return [types.TextContent(type="text", text=output)]

        elif name == "get_seasonal_analysis":
            query = """
                SELECT
                    season,
                    COUNT(*) as transaction_count,
                    SUM(total_amount) as total_revenue,
                    AVG(total_amount) as avg_transaction_value,
                    COUNT(DISTINCT customer_id) as unique_customers,
                    ROUND(CAST(SUM(total_amount) * 100.0 / (SELECT SUM(total_amount) FROM transactions) AS NUMERIC), 2) as revenue_percentage
                FROM transactions
                GROUP BY season
                ORDER BY total_revenue DESC
            """
            results = execute_query(query)

            output = "# Seasonal Analysis\n\n"
            for row in results:
                output += f"""
## {row['season']}
- **Revenue**: {format_currency(row['total_revenue'])} ({row['revenue_percentage']}%)
- **Transactions**: {row['transaction_count']:,}
- **Avg Transaction Value**: {format_currency(row['avg_transaction_value'])}
- **Unique Customers**: {row['unique_customers']:,}
"""
            return [types.TextContent(type="text", text=output)]

        elif name == "get_daily_sales_trend":
            start_date = arguments.get("start_date", "2022-01-01") if arguments else "2022-01-01"
            end_date = arguments.get("end_date", "2023-12-31") if arguments else "2023-12-31"

            query = """
                SELECT
                    sale_date,
                    total_transactions,
                    total_revenue,
                    avg_transaction_value,
                    unique_customers
                FROM daily_sales_summary
                WHERE sale_date BETWEEN %s AND %s
                ORDER BY sale_date
            """
            results = execute_query(query, (start_date, end_date))

            # Summary statistics
            total_rev = sum(float(r['total_revenue']) for r in results)
            total_trans = sum(r['total_transactions'] for r in results)
            avg_daily_rev = total_rev / len(results) if results else 0

            output = f"# Daily Sales Trend ({start_date} to {end_date})\n\n"
            output += f"## Summary\n"
            output += f"- **Total Revenue**: {format_currency(total_rev)}\n"
            output += f"- **Total Transactions**: {total_trans:,}\n"
            output += f"- **Avg Daily Revenue**: {format_currency(avg_daily_rev)}\n"
            output += f"- **Total Days**: {len(results)}\n\n"

            # Show first and last 5 days
            output += "## First 5 Days\n"
            for row in results[:5]:
                output += f"- **{row['sale_date']}**: {format_currency(row['total_revenue'])} ({row['total_transactions']} trans)\n"

            output += "\n## Last 5 Days\n"
            for row in results[-5:]:
                output += f"- **{row['sale_date']}**: {format_currency(row['total_revenue'])} ({row['total_transactions']} trans)\n"

            return [types.TextContent(type="text", text=output)]

        elif name == "get_payment_method_analysis":
            query = """
                SELECT
                    payment_method,
                    COUNT(*) as transaction_count,
                    SUM(total_amount) as total_revenue,
                    AVG(total_amount) as avg_transaction_value,
                    ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions) AS NUMERIC), 2) as transaction_percentage
                FROM transactions
                GROUP BY payment_method
                ORDER BY transaction_count DESC
            """
            results = execute_query(query)

            output = "# Payment Method Analysis\n\n"
            for row in results:
                output += f"""
## {row['payment_method']}
- **Transactions**: {row['transaction_count']:,} ({row['transaction_percentage']}%)
- **Revenue**: {format_currency(row['total_revenue'])}
- **Avg Transaction Value**: {format_currency(row['avg_transaction_value'])}
"""
            return [types.TextContent(type="text", text=output)]

        elif name == "get_hourly_traffic_pattern":
            query = """
                SELECT
                    time_slot,
                    COUNT(*) as transaction_count,
                    SUM(total_amount) as total_revenue,
                    AVG(total_amount) as avg_transaction_value,
                    AVG(checkout_duration_sec) as avg_checkout_time,
                    ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions) AS NUMERIC), 2) as traffic_percentage
                FROM transactions
                GROUP BY time_slot
                ORDER BY transaction_count DESC
            """
            results = execute_query(query)

            output = "# Hourly Traffic Pattern\n\n"
            for row in results:
                output += f"""
## {row['time_slot']}
- **Transactions**: {row['transaction_count']:,} ({row['traffic_percentage']}%)
- **Revenue**: {format_currency(row['total_revenue'])}
- **Avg Transaction Value**: {format_currency(row['avg_transaction_value'])}
- **Avg Checkout Time**: {row['avg_checkout_time']:.0f}s
"""
            return [types.TextContent(type="text", text=output)]

        elif name == "execute_custom_query":
            if not arguments or "query" not in arguments:
                raise ValueError("Query parameter is required")

            query = arguments["query"].strip()

            # Security check: only allow SELECT statements
            if not query.upper().startswith("SELECT"):
                raise ValueError("Only SELECT queries are allowed")

            results = execute_query(query)

            # Format results as markdown table
            if not results:
                return [types.TextContent(type="text", text="No results found")]

            # Get column names
            columns = list(results[0].keys())

            # Create markdown table
            output = "# Custom Query Results\n\n"
            output += "| " + " | ".join(columns) + " |\n"
            output += "| " + " | ".join(["---"] * len(columns)) + " |\n"

            for row in results[:100]:  # Limit to 100 rows
                values = [str(row[col]) if row[col] is not None else "" for col in columns]
                output += "| " + " | ".join(values) + " |\n"

            if len(results) > 100:
                output += f"\n*Showing first 100 of {len(results)} results*\n"

            return [types.TextContent(type="text", text=output)]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        error_msg = f"Error executing {name}: {str(e)}"
        return [types.TextContent(type="text", text=error_msg)]

async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="grocery-analytics",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
