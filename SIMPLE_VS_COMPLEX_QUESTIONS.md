# Simple vs Complex Questions - Smart Answer Length

## 🎯 The Problem You Showed

### Question: "how many stores"

**Bad Answer (Shown)**: 500+ word hallucination about Beverages, STR_002 vs STR_041, ₹163.5M revenue, inventory levels, strategic implications, execution roadmap...

**Expected Answer**: "50 stores" (2 words!)

---

## ✅ The Solution: Smart Question Classification

The new system detects question complexity and adjusts answer length:

### SIMPLE Question → SIMPLE Answer
### COMPLEX Question → DETAILED Answer

---

## 📋 Question Classification

### **SIMPLE QUESTIONS** (Direct Fact Queries)

Pattern: Asking for a single fact/number

Examples:
- "How many stores?"
- "How many stores are present?"
- "Total stores?"
- "Store count?"
- "What is total revenue?"
- "How many categories?"

**Expected Answer**: 1-2 sentences with the number
```
We have 50 stores in total.
```

---

### **AMBIGUOUS QUESTIONS** (Need Clarification)

Pattern: Vague, pronoun-only, or missing entity

Examples:
- "How is it going?"
- "What's happening?"
- "Status?"
- "Best performing?"
- "Compare them"
- "It"

**System Response**: Ask clarifying questions
```
❓ I need clarification to give you the best answer.

What specifically are you asking about?
• Stores (e.g., 'top 5 stores by revenue')
• Categories (e.g., 'how is Beverages performing')
• Customer segments (e.g., 'which segment to prioritize')

Please rephrase your question with more details.
```

---

### **COMPLEX QUESTIONS** (Analysis Required)

Pattern: Asking WHY, HOW, comparison, strategy

Examples:
- "What are the stores that are not performing?"
- "Why is Beverages doing well?"
- "Compare STR_002 vs STR_041"
- "Which customer segment should we prioritize?"
- "How can we improve revenue?"

**Expected Answer**: Executive Summary + Detailed Analysis
```
======================================================================
📊 EXECUTIVE SUMMARY
======================================================================

Bottom 10 stores bleeding ₹15M annually.

**Key Numbers:**
• STR_045: ₹8.2M (worst)
• Gap: ₹6.7M vs top

**Fix This Week:**
1. STR_045 audit by Wed
2. Planogram rollout Friday
3. Launch promo Monday

======================================================================

💡 [EXPAND FOR DETAILED ANALYSIS]

[Full detailed analysis...]
```

---

## 🔍 How the System Detects Question Type

### Detection Logic:

```python
# SIMPLE question detection
is_simple = (
    # Asking for count
    ("how many" in question or "total" in question or "count" in question) and
    # Short question (< 6 words)
    len(question.split()) < 6
)

# AMBIGUOUS question detection
is_ambiguous = (
    # Starts with pronoun
    question.startswith(("it", "they", "that", "this")) or
    # Very vague
    question in ["status", "update", "how are we doing"] or
    # Missing entity in comparison
    ("compare" in question and not has_specific_entities)
)

# COMPLEX question detection
is_complex = (
    # Asks WHY, HOW
    question.startswith(("why", "how can", "what should")) or
    # Asks for strategy
    ("prioritize" in question or "strategy" in question or "improve" in question) or
    # Analysis request
    ("analyze" in question or "not performing" in question)
)
```

---

## 📊 Examples with Expected Outputs

### Example 1: Simple Question

**Q**: "How many stores?"

**Detected**: SIMPLE (count query, 3 words)

**Answer**:
```
We have 50 stores in total.
```
✅ 1 sentence, direct answer

---

### Example 2: Simple Question with Number

**Q**: "Total stores?"

**Detected**: SIMPLE (count query, 2 words)

**Answer**:
```
50 stores total.
```
✅ Minimal answer, just the fact

---

### Example 3: Ambiguous Question

**Q**: "How is it going?"

**Detected**: AMBIGUOUS (pronoun without context, vague)

**Answer**:
```
❓ I need clarification to give you the best answer.

What would you like to know about?
• Store performance (revenue, transactions)
• Category performance (which category?)
• Customer segments (Regular, Premium, etc.)
• Specific metrics (revenue, margins, customers)

Example: 'How are our top stores performing?'
Example: 'What's the revenue for Beverages category?'

Please rephrase your question with more details.
```
✅ Asks for clarification instead of guessing

---

### Example 4: Ambiguous Question - Comparison

**Q**: "Compare them"

**Detected**: AMBIGUOUS (missing entities)

**Answer**:
```
❓ I need clarification to give you the best answer.

What would you like to compare?
Please specify the entities:
• Store IDs (e.g., 'Compare STR_002 vs STR_041')
• Categories (e.g., 'Compare Beverages vs Snacks')
• Time periods (e.g., 'Compare this month vs last month')

Example: 'Compare STR_002 and STR_041 revenue'

Please rephrase your question with more details.
```
✅ Prevents hallucination by asking for specifics

---

### Example 5: Complex Question

**Q**: "What are the stores that are not performing?"

**Detected**: COMPLEX (analysis request, strategy needed)

**Answer**:
```
======================================================================
📊 EXECUTIVE SUMMARY
======================================================================

Bottom 10 stores bleeding ₹15M annually vs top performers.

**Key Numbers:**
• STR_045: ₹8.2M revenue (₹6.7M below average) - worst
• STR_023: ₹8.5M - ATV at ₹386 (₹9 below target)

**Fix This Week:**
1. Call STR_045 manager TODAY - audit by Wed
2. Copy top planogram to bottom 3 by Friday
3. Launch ₹500+ basket incentive Monday

======================================================================

💡 [EXPAND FOR DETAILED ANALYSIS]

──────────────────────────────────────────────────────────────────────
📋 DETAILED ANALYSIS
──────────────────────────────────────────────────────────────────────

[Full analysis with root cause, strategic implications, action plan...]
```
✅ Comprehensive answer with summary + details

---

## 🚀 Answer Length Guidelines

| Question Type | Answer Length | Structure |
|--------------|---------------|-----------|
| **Simple** | 1-2 sentences | Direct fact |
| **Ambiguous** | Clarifying questions | Ask for details |
| **Complex** | Summary + Details | Two-tier format |

### Simple Question Answers:
- 1-2 sentences maximum
- Just the fact requested
- No analysis unless asked
- No strategic implications
- No action plans

### Complex Question Answers:
- Executive Summary (100-150 words)
- Detailed Analysis (400+ words)
- Root cause diagnosis
- Action plan with deadlines
- Execution roadmap

---

## ❌ What NOT to Do (Examples from Bad Answer)

### Bad Response to "How many stores?":

❌ "We are looking at beverage revenue performance..."
❌ "After analyzing data from STR_002 (₹14.92M revenue)..."
❌ "To close this gap, we need to focus on Personal Care..."
❌ "SECTION 2: DETAILED ANALYSIS..."
❌ "SECTION 3: STRATEGIC IMPLICATIONS..."
❌ "SECTION 4: DETAILED ACTION PLAN..."
❌ "SECTION 5: EXECUTION ROADMAP..."

**Why it's bad**:
- Question asks for COUNT
- Answer talks about BEVERAGES (wrong entity!)
- Answer is 500+ words for a 2-word question
- Hallucinating strategic plans nobody asked for

---

## ✅ What TO Do

### Good Response to "How many stores?":

✅ "We have 50 stores in total."

**Why it's good**:
- Directly answers the question
- Correct entity (stores, not beverages)
- Appropriate length (1 sentence)
- No hallucination

---

## 🔍 Detection Patterns

### Simple Question Patterns:
```python
patterns = [
    "how many {entity}",
    "total {entity}",
    "{entity} count",
    "what is {metric}",
    "when {event}"
]

# Examples:
"how many stores" → SIMPLE
"total revenue" → SIMPLE
"store count" → SIMPLE
"what is ATV" → SIMPLE
```

### Ambiguous Question Patterns:
```python
patterns = [
    starts_with_pronoun: ["it", "they", "this", "that"],
    vague_terms: ["status", "update", "how's it going"],
    missing_entity: ["best", "worst", "compare"] without entity
]

# Examples:
"it" → AMBIGUOUS
"status" → AMBIGUOUS
"best performing" → AMBIGUOUS (best what?)
"compare" → AMBIGUOUS (compare what?)
```

### Complex Question Patterns:
```python
patterns = [
    "why {anything}",
    "how can {action}",
    "what should {action}",
    "{entity} not performing",
    "prioritize {entity}",
    "improve {metric}",
    "strategy for {goal}"
]

# Examples:
"why is revenue low" → COMPLEX
"how can we improve" → COMPLEX
"what should we prioritize" → COMPLEX
"stores not performing" → COMPLEX
```

---

## 🎯 System Flow

```
USER QUESTION: "How many stores?"
     ↓
AMBIGUITY CHECKER
  → Is it ambiguous? NO ✓
  → Is it simple? YES ✓
     ↓
QUESTION UNDERSTANDING
  → Entity: store
  → Intent: identify (count)
  → Complexity: SIMPLE
     ↓
ROUTER
  → Load: store_performance
  → Mode: COUNT_ONLY
     ↓
ANALYSIS AGENT (Simple Mode)
  → Count stores in data
  → Generate 1-sentence answer
  → NO detailed analysis
  → NO strategic implications
     ↓
ANSWER: "We have 50 stores in total."
```

vs

```
USER QUESTION: "What are stores not performing?"
     ↓
AMBIGUITY CHECKER
  → Is it ambiguous? NO ✓
  → Is it simple? NO
  → Is it complex? YES ✓
     ↓
QUESTION UNDERSTANDING
  → Entity: store
  → Intent: identify + analyze
  → Complexity: COMPLEX
     ↓
ROUTER
  → Load: store_performance (bottom stores)
  → Mode: FULL_ANALYSIS
     ↓
ANALYSIS AGENT (Full Mode)
  → Identify bottom stores
  → Analyze root causes
  → Strategic implications
  → Action plan
  → Generate Summary + Details
     ↓
ANSWER: [Executive Summary] + [Detailed Analysis]
```

---

## 🚀 Usage

### Run the New System:
```bash
python3 langgraph_ultra_precise_with_clarification.py
```

### Examples:

**Simple Question**:
```
You: How many stores?

Store Manager:
We have 50 stores in total.
```

**Ambiguous Question**:
```
You: How is it going?

Store Manager:
❓ I need clarification to give you the best answer.

What would you like to know about?
• Store performance (revenue, transactions)
• Category performance (which category?)
• Customer segments

Please rephrase your question with more details.
```

**Complex Question**:
```
You: What are stores not performing?

Store Manager:

======================================================================
📊 EXECUTIVE SUMMARY
======================================================================

Bottom 10 stores bleeding ₹15M annually.

[Key insights and actions...]
```

---

## ✅ Benefits

| Before | After |
|--------|-------|
| ❌ 500 words for "how many stores" | ✅ 1 sentence |
| ❌ Hallucinates about Beverages | ✅ Answers about stores |
| ❌ Guesses when ambiguous | ✅ Asks for clarification |
| ❌ Same length for all answers | ✅ Length matches complexity |
| ❌ Generic analysis | ✅ Targeted to question type |

---

## 🎯 Summary

**The New System**:

1. ✅ **Detects Simple Questions** → Gives 1-2 sentence answers
2. ✅ **Detects Ambiguous Questions** → Asks for clarification
3. ✅ **Detects Complex Questions** → Gives Summary + Details
4. ✅ **Never Hallucinates** → Only answers what was asked
5. ✅ **Correct Entity Type** → Stores question = stores answer

**Result**: No more 500-word hallucinations for simple questions!
