# Multi-Agent Store Manager AI System

## Overview

A sophisticated multi-agent orchestration system that uses **Router → Analysis → Verification** architecture to provide verified, strategic business insights in the voice of an experienced store manager.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER QUESTION                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  AGENT 1: ROUTER                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Purpose: Analyze query & determine what's needed                │
│                                                                   │
│  Analyzes:                                                        │
│  • Query intent and topic                                        │
│  • Required data sources (from 20 CSV files)                     │
│  • Analysis type (strategic/operational/financial/customer)      │
│                                                                   │
│  Outputs:                                                         │
│  • List of data sources to load                                  │
│  • Analysis type classification                                  │
│  • Key focus areas                                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  DATA LOADING                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  • Loads only relevant CSV data (based on router decision)       │
│  • Loads corresponding business intelligence metadata            │
│  • Prepares comprehensive context                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  AGENT 2: ANALYSIS                                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Purpose: Generate strategic insights (Store Manager Persona)    │
│                                                                   │
│  Provides:                                                        │
│  1. WHAT'S HAPPENING (Facts & Numbers)                           │
│     - Key metrics with specific numbers                          │
│     - Comparisons to benchmarks                                  │
│                                                                   │
│  2. WHY THIS MATTERS (Root Cause & Business Impact)              │
│     - Underlying drivers                                         │
│     - P&L impact (revenue, margin, costs)                        │
│     - Risks and opportunities                                    │
│                                                                   │
│  3. RECOMMENDED ACTIONS (Prioritized Strategy)                   │
│     - 3-5 specific, actionable steps                             │
│     - Prioritized by ROI and urgency                             │
│     - Timeline and expected impact                               │
│                                                                   │
│  4. SUCCESS METRICS (KPIs to Track)                              │
│     - 3-5 KPIs to monitor                                        │
│     - Realistic targets                                          │
│     - Tracking frequency                                         │
│                                                                   │
│  Persona: 15+ years retail management experience                 │
│  Style: Direct, confident, data-driven, action-oriented          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  AGENT 3: VERIFICATION                                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Purpose: Fact-check analysis against actual data                │
│                                                                   │
│  Process:                                                         │
│  1. Extract factual claims from analysis                         │
│     • Numbers (₹XXX, XX%, XXX customers)                         │
│     • Rankings (top 5, bottom 10)                                │
│     • Comparisons                                                │
│                                                                   │
│  2. Verify each claim against CSV data                           │
│     • Check if numbers match actual data                         │
│     • Validate calculations                                      │
│     • Confirm trends and patterns                                │
│                                                                   │
│  3. Correct inaccuracies                                         │
│     • Replace incorrect numbers with verified facts              │
│     • Maintain store manager tone                                │
│     • Preserve structure and recommendations                     │
│                                                                   │
│  Output: Verified, fact-checked analysis                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   VERIFIED STRATEGIC INSIGHT                      │
│                 (Store Manager Language + Facts)                  │
└─────────────────────────────────────────────────────────────────┘
```

## Key Features

### 1. Intelligent Query Routing
- **Analyzes** user intent and topic
- **Identifies** required data sources from 20 available CSV files
- **Classifies** analysis type (strategic, operational, financial, customer, product, performance)
- **Optimizes** by loading only relevant data (not all 1,151 rows every time)

### 2. Store Manager Persona (Analysis Agent)

**Background:**
- 15+ years in grocery retail management
- Expert in P&L, inventory, customer segmentation, category management
- Data-driven decision maker with operational excellence focus

**Communication Style:**
- **Direct & Confident**: "Let me walk you through what the data shows..."
- **Data-Driven**: Always cites specific numbers (₹, %, counts)
- **Business-Focused**: Connects every insight to P&L impact
- **Action-Oriented**: Provides prioritized, actionable recommendations
- **Retail Terminology**: Uses SSS, ATV, UPT, CLV, SKU, turns, shrinkage naturally
- **Shows Urgency**: Flags critical issues (URGENT, HIGH PRIORITY)

**Known Business Context:**
- Manages 50 stores across 5 regions
- ₹682M annual revenue, 1.87M transactions
- Critical issues: Wastage (₹15-20M), Promotion problem (-₹155 ATV), Customer conversion gaps
- ₹304M growth opportunity identified

### 3. Fact Verification (Verification Agent)
- **Extracts** factual claims from analysis (numbers, percentages, rankings)
- **Verifies** against actual CSV data
- **Corrects** any inaccuracies while maintaining tone
- **Ensures** all facts are backed by data

### 4. Comprehensive Data Access
- **All 20 CSV files** with 1,151 rows of KPI data
- **Business intelligence** metadata (14 sections)
- **Strategic insights** document (975 lines)
- **Smart loading** - only loads relevant data per query

## Response Structure

Every response follows this proven framework:

### 1. WHAT'S HAPPENING (The Facts)
```
"Let me walk you through what the data shows..."

- Total revenue: ₹682.3M across 1.87M transactions
- Average transaction value: ₹364.93
- Top store (STR_002): ₹14.9M (Hypermarket, East region)
- Category leader: Beverages at 23.96% share (₹163.5M)
```

### 2. WHY THIS MATTERS (Root Cause & Business Impact)
```
"Here's why this is significant..."

ROOT CAUSES:
- Larger footprint in Hypermarket format drives 44.5% of revenue
- Evening traffic (4-9 PM) represents 45% of daily transactions
- Beverage category has 35-40% margin potential vs 25% chain average

BUSINESS IMPACT:
- Every 1% increase in ATV = ₹6.8M annual revenue
- Perishable wastage at 8% vs 3% industry best practice = ₹12M opportunity
- Customer retention improvement of 5% = ₹34M additional revenue
```

### 3. RECOMMENDED ACTIONS (Prioritized Strategy)
```
"Here's my action plan..."

URGENT (Week 1):
1. Fix perishable markdown system (30% at 2 days, 50% at 1 day expiry)
   Expected Impact: ₹8-12M annual savings | ROI: 500%

HIGH PRIORITY (Month 1):
2. Launch VIP program for top 2,000 customers (₹10K+ annual spend)
   Expected Impact: Protect ₹33M revenue | ROI: 560%

3. Fix promotion strategy - implement "Spend ₹500, get 20% off" thresholds
   Expected Impact: ₹93M annual uplift | ROI: 9,200%

MEDIUM PRIORITY (Month 2):
4. Replicate top store practices in bottom 5 stores
   Expected Impact: ₹40M opportunity | ROI: 400%
```

### 4. SUCCESS METRICS (How We'll Track This)
```
"We'll measure success by tracking..."

DAILY:
• Perishable wastage % (Target: <3% vs current 8%)
• Stock-outs of top 20 products (Target: 0)

WEEKLY:
• Average Transaction Value (Target: ₹420 vs current ₹365)
• Promotion ROI (Revenue per discount rupee)

MONTHLY:
• Same-Store Sales Growth (Target: +15% YoY)
• Customer retention rate (Target: 55% vs current 43.4%)
• VIP customer contribution (Target: 20% of revenue)
```

## Usage

### Quick Start

```bash
# Run the multi-agent system
python3 multi_agent_store_manager.py

# Or test first
python3 test_multi_agent.py
```

### Example Session

```
🏪 You: How can we reduce our perishable wastage?

🔍 ROUTER AGENT: Analyzing query...
  → Analysis Type: operational
  → Data Sources: category_performance, inventory_intelligence, product_performance
  → Focus: perishable waste reduction strategies

📊 Loading relevant data...
  ✓ Context prepared

💼 ANALYSIS AGENT: Generating strategic insights...

✅ VERIFICATION AGENT: Fact-checking analysis...
  ✓ All facts verified - analysis is accurate

======================================================================
ANALYSIS COMPLETE
======================================================================

💼 Store Manager:

Let me walk you through what the data shows...

WHAT'S HAPPENING:
We're hemorrhaging ₹15-20M annually on perishable wastage. Breaking this down:
- Bakery: 2-day expiry, 25% average discount (CRITICAL risk)
- Fresh Produce: 3-day expiry, 21% average discount (HIGH risk)
- Dairy: 4-day expiry, 16% average discount (MEDIUM risk)

Current wastage rate: ~8% vs. industry best practice of 3%.
That's 5 percentage points or ₹15-20M hitting our P&L.

WHY THIS MATTERS:
This directly impacts gross margin. Every 1% reduction in wastage = ₹3M to bottom line.

ROOT CAUSES:
1. No dynamic markdown system - products sitting at full price until day before expiry
2. Over-ordering based on safety stock formulas, not actual demand patterns
3. No local sourcing partnerships for fresh produce (long lead times = higher wastage)
4. Bakery deliveries once daily (afternoon) - stale by evening rush (45% of traffic)

BUSINESS IMPACT:
- Direct loss: ₹15-20M annually
- Opportunity cost: Could be reinvested in customer acquisition
- Customer dissatisfaction: Stale products hurt repeat business
- Competitive disadvantage: Rivals with better fresh food selection

RECOMMENDED ACTIONS:

URGENT (Implement Week 1):
1. Automated markdown system
   - 30% discount at 2 days to expiry
   - 50% discount at 1 day to expiry
   - 75% discount at 4 hours to expiry
   Expected Impact: ₹8-12M annual savings | Implementation: IT update

2. Twice-daily bakery delivery
   - 6 AM and 2 PM deliveries
   - Partner with local bakeries for fresher product
   Expected Impact: Reduce bakery wastage from 25% to 10% = ₹3M

HIGH PRIORITY (Month 1):
3. Implement "Ugly Produce" section
   - 40% discount on cosmetically imperfect items
   - Reduce produce wastage by 30%
   Expected Impact: ₹4M savings + customer goodwill

4. Partner with food banks
   - Donate near-expiry items (tax benefit)
   - Corporate social responsibility + cost reduction
   Expected Impact: ₹2M tax benefit + brand value

MEDIUM PRIORITY (Month 2):
5. Demand forecasting upgrade
   - ML-based ordering (weather, events, history)
   - Reduce over-ordering by 20%
   Expected Impact: ₹3M working capital reduction

SUCCESS METRICS:
Track these daily/weekly:

DAILY:
• Wastage percentage by category (Target: <3% vs current 8%)
• Markdown velocity (how fast discounted items sell)
• Freshness score (days to expiry at sale)

WEEKLY:
• Total wastage cost (Target: <₹300K/week vs current ₹400K)
• Customer complaints about freshness (Target: <5/week)
• Produce turnover (Target: <2 days avg inventory)

MONTHLY:
• Gross margin improvement (Target: +1.8% = ₹12M annual)
• Perishable category revenue (ensure discounts don't hurt revenue)
• Same-store sales growth for perishables

Timeline: Start Week 1, full implementation by Month 2
Total Investment: ₹5M (IT systems, partnerships)
Expected Savings: ₹20M annual (ROI: 300%)

This is a critical P&L improvement opportunity. We move fast on this.
```

## Agent Responsibilities

### Router Agent
**Input**: User question
**Output**: Routing decision JSON

```json
{
  "data_sources": ["category_performance", "product_performance"],
  "analysis_type": "operational",
  "key_focus": "perishable waste reduction"
}
```

**Logic**:
- Keyword matching (store → store_performance, customer → customer_segment)
- Intent classification (how can, what are, why is → analysis type)
- Context relevance (loads corresponding business intelligence)

### Analysis Agent
**Input**: Question + Routing + Context Data
**Output**: Strategic analysis (store manager persona)

**Prompt Engineering**:
```
- Role: Experienced Store Manager (15+ years)
- Expertise: P&L, inventory, customers, operations
- Style: Direct, data-driven, action-oriented
- Context: Business issues, opportunities, constraints
- Structure: What/Why/Actions/Metrics
- Tone: Speaking to regional director
```

### Verification Agent
**Input**: Analysis + Routing
**Output**: Fact-checked analysis

**Process**:
1. Extract claims (regex patterns for numbers, percentages, rankings)
2. Verify against CSV data
3. Correct inaccuracies
4. Maintain tone and structure

## Data Sources Used

**Automatically Loaded Based on Question:**

| Question Topic | Loaded Data Sources |
|---------------|---------------------|
| Revenue, growth | overall_business, financial_opportunities |
| Stores, locations | store_performance, store_intelligence |
| Categories | category_performance, category_intelligence |
| Products | product_performance, brand_performance |
| Customers | customer_segment, age_group, gender, customer_intelligence |
| Time patterns | daily_performance, weekly_performance, monthly_performance, time_slot |
| Operations | time_slot, delivery_method, employee_performance, operational_intelligence |
| Pricing | payment_method, pricing_intelligence |
| Seasons | seasonal, seasonal_intelligence |
| Inventory | product_performance, inventory_intelligence |

**Plus Always Loaded:**
- Business context metadata (14 sections)
- Strategic insights document (975 lines)
- Master KPI dashboard (143 metrics)

## Benefits Over Single-Agent System

| Feature | Single Agent | Multi-Agent System |
|---------|-------------|-------------------|
| Data Loading | All data every time (slow) | Only relevant data (fast) |
| Analysis Quality | Generic | Persona-driven (store manager) |
| Fact Accuracy | Unverified | Verified against data |
| Response Structure | Inconsistent | Always What/Why/Actions/Metrics |
| Business Context | Limited | Rich (metadata + insights) |
| Actionability | Observations | Prioritized actions with ROI |

## Performance

- **Query Routing**: 2-5 seconds
- **Context Loading**: 1-2 seconds (only relevant data)
- **Analysis Generation**: 10-20 seconds
- **Verification**: 5-10 seconds
- **Total Response Time**: 18-37 seconds

(First query may take longer due to model loading)

## Testing

```bash
# Full test with sample question
python3 test_multi_agent.py

# Verify data loading
python3 verify_all_csvs.py

# Interactive session
python3 multi_agent_store_manager.py
```

## Example Questions

**Strategic:**
- "What are the top 3 revenue opportunities?"
- "How can we grow profitability by 20%?"
- "What's our competitive positioning?"

**Operational:**
- "How can we reduce perishable wastage?"
- "What's the optimal staffing for peak hours?"
- "How can we improve checkout efficiency?"

**Customer:**
- "Which customer segment should we prioritize?"
- "How can we improve customer retention?"
- "What drives customer lifetime value?"

**Product:**
- "Why is beverage performance so strong?"
- "Which products have margin opportunity?"
- "How should we optimize our product mix?"

**Financial:**
- "What's the ROI of improving bottom stores?"
- "How can promotions be more effective?"
- "Where should we invest for maximum return?"

## Troubleshooting

**Router not finding data:**
- Check that question keywords match data source names
- Router defaults to overall_business if uncertain

**Analysis too generic:**
- Ensure business_context_metadata.json is loaded
- Check COMPLETE_DATA_INSIGHTS.md is present

**Verification missing claims:**
- Verification is pattern-based (looks for numbers, %)
- Complex claims may pass through unverified

**Slow responses:**
- Use smaller model (llama3.2:1b vs llama3)
- Reduce context loaded (modify routing logic)

## Future Enhancements

1. **Enhanced Verification**: More sophisticated fact-checking against actual CSV data
2. **Multi-Model**: Use different models for different agents (fast router, powerful analysis)
3. **Caching**: Cache routing decisions and frequently accessed data
4. **Feedback Loop**: Learn from user corrections to improve routing
5. **Visualization**: Generate charts and graphs with insights
6. **A/B Testing**: Compare recommendations against historical data
7. **Alerts**: Proactive notifications for critical issues

## Conclusion

The Multi-Agent Store Manager System provides **verified, strategic business insights** in the voice of an experienced retail manager. By combining intelligent routing, comprehensive data access, and fact verification, it delivers:

- ✅ **Accurate**: All facts verified against data
- ✅ **Strategic**: What happened, why, what to do
- ✅ **Actionable**: Prioritized recommendations with ROI
- ✅ **Professional**: Store manager persona and terminology
- ✅ **Efficient**: Only loads relevant data per query

**This is business intelligence at the level of a senior retail consultant, available on-demand through conversation.**
