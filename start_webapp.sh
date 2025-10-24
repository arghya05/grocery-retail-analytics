#!/bin/bash

echo "======================================================================"
echo "🚀 GROCERY ANALYTICS WEB APP"
echo "======================================================================"
echo ""
echo "Starting the web application..."
echo ""
echo "📊 Database: grocery_analytics"
echo "🌐 Web URL: http://localhost:5000"
echo ""
echo "======================================================================"
echo ""

# Check if PostgreSQL is running
if ! pg_isready -q; then
    echo "⚠️  PostgreSQL is not running!"
    echo "   Starting PostgreSQL..."
    brew services start postgresql@14
    sleep 2
fi

# Check if database exists
if ! psql -lqt | cut -d \| -f 1 | grep -qw grocery_analytics; then
    echo "⚠️  Database 'grocery_analytics' not found!"
    echo "   Please run: python load_data_to_postgres.py"
    exit 1
fi

echo "✅ Database ready!"
echo ""
echo "🌐 Starting web server on http://localhost:5000"
echo ""
echo "💡 Try asking questions like:"
echo "   - Show me the sales summary"
echo "   - What are the top 10 products?"
echo "   - Analyze customer segments"
echo "   - Which season has highest revenue?"
echo ""
echo "======================================================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask app
python web_app.py
