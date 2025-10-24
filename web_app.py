#!/usr/bin/env python3
"""
Grocery Analytics Web Application
Simple web interface to query grocery data using natural language
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database connection parameters
DB_PARAMS = {
    'dbname': 'grocery_analytics',
    'user': 'arghya.mukherjee',
    'password': '',
    'host': 'localhost',
    'port': '5432'
}

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

def interpret_question(question):
    """Interpret natural language question and route to appropriate query"""
    question_lower = question.lower()

    # Sales summary
    if any(word in question_lower for word in ['summary', 'overview', 'total revenue', 'total sales', 'business metrics']):
        return 'sales_summary', {}

    # Top products
    elif any(word in question_lower for word in ['top product', 'best product', 'best seller', 'top selling']):
        limit = 10
        if 'top 5' in question_lower or 'best 5' in question_lower:
            limit = 5
        elif 'top 20' in question_lower or 'best 20' in question_lower:
            limit = 20
        return 'top_products', {'limit': limit}

    # Category performance
    elif any(word in question_lower for word in ['category', 'categories', 'product type']):
        return 'category_performance', {}

    # Customer insights
    elif any(word in question_lower for word in ['customer', 'vip', 'segment', 'buyer']):
        segment = 'all'
        if 'regular' in question_lower:
            segment = 'Regular'
        elif 'premium' in question_lower:
            segment = 'Premium'
        elif 'occasional' in question_lower:
            segment = 'Occasional'
        elif 'new' in question_lower:
            segment = 'New'
        return 'customer_insights', {'segment': segment}

    # Store performance
    elif any(word in question_lower for word in ['store', 'shop', 'outlet', 'location']):
        return 'store_performance', {}

    # Seasonal analysis
    elif any(word in question_lower for word in ['season', 'winter', 'summer', 'monsoon', 'spring']):
        return 'seasonal_analysis', {}

    # Payment methods
    elif any(word in question_lower for word in ['payment', 'upi', 'cash', 'card', 'wallet']):
        return 'payment_analysis', {}

    # Traffic pattern
    elif any(word in question_lower for word in ['traffic', 'busy', 'peak', 'hour', 'time']):
        return 'traffic_pattern', {}

    # Daily trend
    elif any(word in question_lower for word in ['daily', 'trend', 'date', 'day by day']):
        return 'daily_trend', {}

    # Default to sales summary
    else:
        return 'general_search', {'question': question}

def get_sales_summary():
    """Get overall sales summary"""
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

    return {
        'type': 'summary',
        'data': {
            'Total Revenue': format_currency(data.get('total_revenue')),
            'Total Transactions': f"{data.get('total_transactions'):,}",
            'Average Transaction': format_currency(data.get('avg_transaction_value')),
            'Total Items Sold': f"{data.get('total_items_sold'):,}",
            'Unique Customers': f"{data.get('unique_customers'):,}",
            'Unique Products': str(data.get('unique_products')),
            'Period': f"{data.get('start_date')} to {data.get('end_date')}"
        }
    }

def get_top_products(limit=10):
    """Get top selling products"""
    query = """
        SELECT
            product_name,
            category,
            brand,
            total_revenue,
            total_units_sold,
            transaction_count
        FROM top_products
        ORDER BY total_revenue DESC
        LIMIT %s
    """
    results = execute_query(query, (limit,))

    data = []
    for idx, row in enumerate(results, 1):
        data.append({
            'Rank': idx,
            'Product': row['product_name'],
            'Category': row['category'],
            'Revenue': format_currency(row['total_revenue']),
            'Units Sold': f"{row['total_units_sold']:,}",
            'Transactions': f"{row['transaction_count']:,}"
        })

    return {
        'type': 'table',
        'title': f'Top {limit} Products by Revenue',
        'data': data
    }

def get_category_performance():
    """Get category performance"""
    query = """
        SELECT
            category,
            total_revenue,
            transaction_count,
            total_units_sold,
            revenue_percentage
        FROM category_performance
        ORDER BY total_revenue DESC
    """
    results = execute_query(query)

    data = []
    for idx, row in enumerate(results, 1):
        data.append({
            'Rank': idx,
            'Category': row['category'],
            'Revenue': format_currency(row['total_revenue']),
            'Revenue %': f"{row['revenue_percentage']}%",
            'Transactions': f"{row['transaction_count']:,}",
            'Units Sold': f"{row['total_units_sold']:,}"
        })

    return {
        'type': 'table',
        'title': 'Category Performance',
        'data': data
    }

def get_customer_insights(segment='all'):
    """Get customer insights"""
    if segment == 'all':
        query = """
            SELECT
                customer_type,
                COUNT(*) as customer_count,
                SUM(visit_count) as total_visits,
                SUM(lifetime_value) as total_revenue,
                AVG(lifetime_value) as avg_lifetime_value,
                AVG(visit_count) as avg_visits
            FROM customer_insights
            GROUP BY customer_type
            ORDER BY total_revenue DESC
        """
        results = execute_query(query)
    else:
        query = """
            SELECT
                customer_type,
                COUNT(*) as customer_count,
                SUM(visit_count) as total_visits,
                SUM(lifetime_value) as total_revenue,
                AVG(lifetime_value) as avg_lifetime_value,
                AVG(visit_count) as avg_visits
            FROM customer_insights
            WHERE customer_type = %s
            GROUP BY customer_type
        """
        results = execute_query(query, (segment,))

    data = []
    for row in results:
        data.append({
            'Segment': row['customer_type'],
            'Customers': f"{row['customer_count']:,}",
            'Total Revenue': format_currency(row['total_revenue']),
            'Avg Lifetime Value': format_currency(row['avg_lifetime_value']),
            'Avg Visits': f"{row['avg_visits']:.2f}"
        })

    return {
        'type': 'table',
        'title': f'Customer Insights{" - " + segment if segment != "all" else ""}',
        'data': data
    }

def get_store_performance():
    """Get store performance"""
    query = """
        SELECT
            store_id,
            store_region,
            store_type,
            total_revenue,
            transaction_count,
            unique_customers
        FROM store_performance
        ORDER BY total_revenue DESC
        LIMIT 10
    """
    results = execute_query(query)

    data = []
    for idx, row in enumerate(results, 1):
        data.append({
            'Rank': idx,
            'Store': row['store_id'],
            'Region': row['store_region'],
            'Type': row['store_type'],
            'Revenue': format_currency(row['total_revenue']),
            'Transactions': f"{row['transaction_count']:,}",
            'Customers': f"{row['unique_customers']:,}"
        })

    return {
        'type': 'table',
        'title': 'Top 10 Stores by Revenue',
        'data': data
    }

def get_seasonal_analysis():
    """Get seasonal analysis"""
    query = """
        SELECT
            season,
            COUNT(*) as transaction_count,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_transaction_value,
            ROUND(CAST(SUM(total_amount) * 100.0 / (SELECT SUM(total_amount) FROM transactions) AS NUMERIC), 2) as revenue_percentage
        FROM transactions
        GROUP BY season
        ORDER BY total_revenue DESC
    """
    results = execute_query(query)

    data = []
    for row in results:
        data.append({
            'Season': row['season'],
            'Revenue': format_currency(row['total_revenue']),
            'Revenue %': f"{row['revenue_percentage']}%",
            'Transactions': f"{row['transaction_count']:,}",
            'Avg Transaction': format_currency(row['avg_transaction_value'])
        })

    return {
        'type': 'table',
        'title': 'Seasonal Performance',
        'data': data
    }

def get_payment_analysis():
    """Get payment method analysis"""
    query = """
        SELECT
            payment_method,
            COUNT(*) as transaction_count,
            SUM(total_amount) as total_revenue,
            ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions) AS NUMERIC), 2) as transaction_percentage
        FROM transactions
        GROUP BY payment_method
        ORDER BY transaction_count DESC
    """
    results = execute_query(query)

    data = []
    for row in results:
        data.append({
            'Payment Method': row['payment_method'],
            'Transactions': f"{row['transaction_count']:,}",
            'Transaction %': f"{row['transaction_percentage']}%",
            'Revenue': format_currency(row['total_revenue'])
        })

    return {
        'type': 'table',
        'title': 'Payment Method Analysis',
        'data': data
    }

def get_traffic_pattern():
    """Get hourly traffic pattern"""
    query = """
        SELECT
            time_slot,
            COUNT(*) as transaction_count,
            SUM(total_amount) as total_revenue,
            ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions) AS NUMERIC), 2) as traffic_percentage
        FROM transactions
        GROUP BY time_slot
        ORDER BY transaction_count DESC
    """
    results = execute_query(query)

    data = []
    for row in results:
        data.append({
            'Time Slot': row['time_slot'],
            'Transactions': f"{row['transaction_count']:,}",
            'Traffic %': f"{row['traffic_percentage']}%",
            'Revenue': format_currency(row['total_revenue'])
        })

    return {
        'type': 'table',
        'title': 'Hourly Traffic Pattern',
        'data': data
    }

def get_daily_trend():
    """Get daily sales trend (last 30 days)"""
    query = """
        SELECT
            sale_date,
            total_transactions,
            total_revenue
        FROM daily_sales_summary
        ORDER BY sale_date DESC
        LIMIT 30
    """
    results = execute_query(query)

    data = []
    for row in results:
        data.append({
            'Date': str(row['sale_date']),
            'Transactions': f"{row['total_transactions']:,}",
            'Revenue': format_currency(row['total_revenue'])
        })

    return {
        'type': 'table',
        'title': 'Daily Sales Trend (Last 30 Days)',
        'data': data[::-1]  # Reverse to show oldest first
    }

def general_search(question):
    """Handle general questions with smart search"""
    # Try to find relevant information
    query = """
        SELECT
            category,
            SUM(total_amount) as revenue,
            COUNT(*) as transactions
        FROM transactions
        GROUP BY category
        ORDER BY revenue DESC
        LIMIT 5
    """
    results = execute_query(query)

    data = []
    for row in results:
        data.append({
            'Category': row['category'],
            'Revenue': format_currency(row['revenue']),
            'Transactions': f"{row['transactions']:,}"
        })

    return {
        'type': 'table',
        'title': 'Top 5 Categories (General Search)',
        'message': f'I found some general insights for your question: "{question}"',
        'data': data
    }

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Handle question from frontend"""
    try:
        data = request.json
        question = data.get('question', '').strip()

        if not question:
            return jsonify({'error': 'Please ask a question'}), 400

        # Interpret the question
        query_type, params = interpret_question(question)

        # Route to appropriate handler
        if query_type == 'sales_summary':
            result = get_sales_summary()
        elif query_type == 'top_products':
            result = get_top_products(params.get('limit', 10))
        elif query_type == 'category_performance':
            result = get_category_performance()
        elif query_type == 'customer_insights':
            result = get_customer_insights(params.get('segment', 'all'))
        elif query_type == 'store_performance':
            result = get_store_performance()
        elif query_type == 'seasonal_analysis':
            result = get_seasonal_analysis()
        elif query_type == 'payment_analysis':
            result = get_payment_analysis()
        elif query_type == 'traffic_pattern':
            result = get_traffic_pattern()
        elif query_type == 'daily_trend':
            result = get_daily_trend()
        else:
            result = general_search(question)

        return jsonify({
            'success': True,
            'question': question,
            'result': result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """Get sample questions"""
    suggestions = [
        "Show me the sales summary",
        "What are the top 10 products?",
        "Analyze customer segments",
        "Which season has highest revenue?",
        "Show store performance",
        "What are the payment method trends?",
        "Show me hourly traffic patterns",
        "What's the category performance?",
        "Show me top 20 best sellers",
        "Analyze premium customers"
    ]
    return jsonify({'suggestions': suggestions})

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 GROCERY ANALYTICS WEB APP")
    print("=" * 60)
    print("\n📊 Starting server...")
    print("   URL: http://localhost:5000")
    print("\n💡 Ask questions like:")
    print("   - Show me the sales summary")
    print("   - What are the top 10 products?")
    print("   - Analyze customer segments")
    print("   - Which season has highest revenue?")
    print("\n✅ Server ready! Open http://localhost:5000 in your browser")
    print("=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
