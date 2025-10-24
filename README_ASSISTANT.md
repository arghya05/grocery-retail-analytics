# Store Manager AI Assistant

An interactive command-line assistant that uses Ollama to provide intelligent insights about your grocery store data. The assistant acts as an experienced store manager, analyzing KPI data and providing actionable recommendations.

## Features

- **Interactive Q&A**: Ask questions in natural language
- **Store Manager Persona**: Responses from the perspective of an experienced store manager
- **Comprehensive Context**: Uses all 19 KPI datasets for accurate insights
- **Smart Context Selection**: Automatically selects relevant data based on your question
- **Actionable Insights**: Provides WHAT happened, WHY it happened, and WHAT to do

## Prerequisites

### 1. Install Ollama

Download and install Ollama from: https://ollama.ai

### 2. Install a Model

After installing Ollama, pull a language model:

```bash
# Recommended: Llama 3 (best performance)
ollama pull llama3

# Alternative: Llama 2
ollama pull llama2

# Alternative: Mistral
ollama pull mistral
```

### 3. Start Ollama Server

```bash
ollama serve
```

Keep this running in a separate terminal.

### 4. Install Python Dependencies

```bash
pip install pandas requests
```

## Usage

### Start the Assistant

```bash
python store_manager_assistant.py
```

Or if you made it executable:

```bash
./store_manager_assistant.py
```

### Example Questions

**Store Performance:**
- "What are our top performing stores and why?"
- "Which region is underperforming and what should we do?"
- "Compare Hypermarket vs Supermarket vs Express stores"

**Category & Products:**
- "Why is the beverage category performing so well?"
- "What are our top 5 products and their contribution to revenue?"
- "Which categories need attention?"

**Customer Insights:**
- "Which customer segment should we focus on?"
- "What's driving Premium customer spending?"
- "How do different age groups shop with us?"

**Operational:**
- "When are our peak hours and why?"
- "Should we staff more on weekends or weekdays?"
- "What payment methods do customers prefer?"
- "How can we improve checkout times?"

**Time-Based:**
- "How do sales vary by season?"
- "What's the weekend vs weekday performance?"
- "Which months are strongest?"

**Strategic:**
- "How can we increase organic product sales?"
- "Should we focus on home delivery or in-store?"
- "What's our discount strategy impact?"

### Exit the Assistant

Type `quit`, `exit`, or `q` to end the session.

## How It Works

1. **Data Loading**: Loads all KPI CSV files into memory
2. **Context Building**: Creates comprehensive business context
3. **Smart Filtering**: Identifies relevant data based on your question
4. **LLM Analysis**: Sends context + question to Ollama
5. **Store Manager Response**: Returns insights with what/why/what-to-do

## Data Sources

The assistant uses these KPI files:
- `store_manager_kpi_dashboard.csv` - Comprehensive KPI summary
- `kpi_overall_business.csv` - Overall business metrics
- `kpi_store_performance.csv` - Store-wise performance
- `kpi_category_performance.csv` - Category analysis
- `kpi_product_performance.csv` - Top products
- `kpi_customer_segment.csv` - Customer segments
- `kpi_monthly_performance.csv` - Monthly trends
- `kpi_payment_method.csv` - Payment preferences
- `kpi_time_slot.csv` - Peak hours
- `kpi_delivery_method.csv` - Delivery channels
- `kpi_weekend_weekday.csv` - Day type comparison
- `kpi_age_group.csv` - Age demographics
- `kpi_gender.csv` - Gender analysis
- `kpi_seasonal.csv` - Seasonal trends
- `kpi_brand_performance.csv` - Brand analysis
- `kpi_organic_vs_nonorganic.csv` - Product type comparison
- `kpi_employee_performance.csv` - Employee metrics

## Troubleshooting

### "Cannot connect to Ollama"
- Make sure Ollama is running: `ollama serve`
- Check if Ollama is accessible: `curl http://localhost:11434/api/tags`

### "Model not found"
- Pull a model first: `ollama pull llama2`
- List available models: `ollama list`

### "Request timed out"
- The question might be too complex
- Try a more specific question
- Use a smaller/faster model like `mistral`

### Slow responses
- Normal for first query (model loading)
- Subsequent queries are faster
- Consider using a smaller model for speed

## Tips for Best Results

1. **Be Specific**: "Why did beverages perform well?" vs "Tell me about beverages"
2. **Ask for Comparisons**: "Compare weekend vs weekday sales"
3. **Request Recommendations**: "What should we do to improve X?"
4. **Focus on One Topic**: Better results with focused questions
5. **Use Business Terms**: The assistant understands retail terminology

## Configuration

Edit the script to customize:

```python
# Change Ollama URL (if not localhost)
assistant = StoreManagerAssistant(
    ollama_url="http://localhost:11434",
    model="llama3"
)
```

## Performance

- **First Query**: 10-30 seconds (model loading)
- **Subsequent Queries**: 3-10 seconds
- **Context Loading**: 1-2 seconds
- **Memory Usage**: ~500MB (with all CSV data)

## Notes

- All responses are generated by AI and should be validated
- The assistant analyzes historical data only
- Use insights as a starting point for decision-making
- Combine AI insights with domain expertise

## Example Session

```
🏪 You: What are our top performing stores?

⏳ Analyzing data and generating insights...

📊 Store Manager:

WHAT HAPPENED:
Our top performing store is STR_002, an East Region Hypermarket generating
$14.9M in revenue. This is followed by STR_014 ($14.8M) and STR_007 ($14.7M).
Hypermarket format stores dominate our top performers, accounting for
$304M total (44.5% of total revenue).

WHY IT HAPPENED:
1. Hypermarkets have larger footprints allowing more SKUs and categories
2. East region has strong customer base with 199,981 unique customers
3. These stores have higher basket sizes (avg 13.04 items)
4. Strategic locations with good foot traffic

WHAT TO DO:
1. Study STR_002's best practices and replicate across other stores
2. Consider converting high-potential Supermarkets to Hypermarket format
3. Focus on East region expansion given strong performance
4. Invest in training for underperforming stores using top store playbooks
```
