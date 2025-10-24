# Quick Reference: What You Can Customize

## 📝 Main Prompt Template

**File**: `store_manager_prompt_template.txt`

**What it controls**:
- Response format (bullet points, sections, structure)
- Tone and style (brief vs detailed)
- Emojis and formatting
- Examples and quality standards
- Instructions to the AI

**How to edit**:
```bash
nano store_manager_prompt_template.txt
# Make changes, save, restart app
```

**Key sections you can modify**:
1. **CRITICAL INSTRUCTIONS** - Change how AI behaves
2. **RESPONSE FORMAT** - Change output structure
3. **QUALITY EXAMPLE** - Show AI what you want
4. **FORMATTING RULES** - Change bullet styles, emojis
5. **EMOJIS TO USE** - Change or remove emojis

---

## 🧠 Metadata & Domain Knowledge

**File**: `store_manager_metadata_layer.json`

**What it controls**:
- Business context (stores, revenue, regions)
- Retail expertise (inventory, pricing, customer management)
- Category intelligence (margins, strategies)
- Customer segmentation strategies
- Operational best practices
- Strategic recommendations with ROI

**What you can customize**:
- `persona.role` - Change the expert role
- `persona.experience_level` - Adjust years of experience
- `expertise_areas` - Add/remove areas of expertise
- `key_performance_metrics` - Update KPIs and targets
- `strategic_recommendations` - Modify initiatives and ROI
- `retail_expertise_knowledge_base` - Add industry best practices

**Example edit**:
```json
{
  "persona": {
    "role": "Senior Regional Manager & Operations Director",
    "experience_level": "25+ years in multi-channel retail"
  }
}
```

---

## 📊 Data Sources

**Files**: All CSV files in the directory

**What they control**:
- Actual business data the AI analyzes
- KPIs, metrics, store performance
- Customer segments, product performance

**You can**:
- Replace with your own data
- Add new CSV files
- Modify existing metrics

---

## 🎨 Web Interface

**File**: `store_manager_app.py`

**What you can customize**:
- Quick action buttons (line 145-185)
- Business overview stats (line 102-125)
- Key insights section (line 128-139)
- Colors and styling (line 25-86)

**Example**: Add a new quick action button:
```python
if st.button("🔥 What's our biggest issue?", key="critical_issue"):
    st.session_state.current_question = "What's our biggest issue?"
```

---

## 🚀 Quick Customization Examples

### 1. Change Response Style to Detailed

**Edit**: `store_manager_prompt_template.txt`

**Change**:
```
2. Be BRIEF and use BULLET POINTS
```

**To**:
```
2. Provide detailed analysis with supporting context
```

### 2. Add a New Section to Output

**Edit**: `store_manager_prompt_template.txt`

**Add after TRACK DAILY/WEEKLY**:
```
**💰 FINANCIAL IMPACT**
• Revenue impact: ₹X
• Margin impact: X%
• ROI: X%
• Payback period: X months
```

### 3. Change Persona

**Edit**: `store_manager_metadata_layer.json`

**Change**:
```json
"persona": {
  "role": "CFO & Financial Analyst",
  "experience_level": "15+ years in retail finance"
}
```

### 4. Add Custom Domain Knowledge

**Edit**: `store_manager_metadata_layer.json`

**Add to retail_expertise_knowledge_base**:
```json
"supply_chain_management": {
  "lead_times": "Local: 1-2 days, National: 3-5 days, Imported: 14-30 days",
  "order_frequency": "Perishables: Daily, Staples: Weekly, Premium: Bi-weekly"
}
```

### 5. Add New Quick Action in UI

**Edit**: `store_manager_app.py` (around line 150)

**Add**:
```python
if st.button("⚡ Give me a quick win", key="quick_win"):
    st.session_state.current_question = "What's one thing I can do today for immediate impact?"
```

---

## 📁 File Structure

```
sd/
├── store_manager_prompt_template.txt        ← Main prompt (EDIT THIS FIRST)
├── store_manager_metadata_layer.json        ← Domain knowledge
├── store_manager_app.py                     ← Web interface
├── langgraph_multi_agent_store_manager.py   ← AI system (advanced)
├── COMPLETE_DATA_INSIGHTS.md                ← Insights reference
├── PROMPT_CUSTOMIZATION_GUIDE.md            ← Detailed guide
├── CUSTOMIZATION_QUICK_REFERENCE.md         ← This file
└── [All CSV files]                          ← Data sources
```

---

## ⚡ Quick Edit Workflow

1. **Want to change AI response format?**
   → Edit `store_manager_prompt_template.txt`

2. **Want to add domain expertise?**
   → Edit `store_manager_metadata_layer.json`

3. **Want to add quick action buttons?**
   → Edit `store_manager_app.py`

4. **After any edit**:
   ```bash
   # Stop current app (Ctrl+C if running in terminal)
   # Or kill the background process

   # Restart
   streamlit run store_manager_app.py
   ```

---

## 🧪 Testing Your Changes

**Step 1**: Make ONE small change
**Step 2**: Restart app
**Step 3**: Ask a test question: "What are the top 3 stores?"
**Step 4**: Check if output matches your expectation
**Step 5**: Iterate

---

## 💾 Backup Before Major Changes

```bash
# Backup prompt template
cp store_manager_prompt_template.txt store_manager_prompt_template.backup

# Backup metadata
cp store_manager_metadata_layer.json store_manager_metadata_layer.backup

# Restore if needed
cp store_manager_prompt_template.backup store_manager_prompt_template.txt
```

---

## 🆘 Common Issues

### Issue: AI gives generic answers

**Fix**: Edit `store_manager_prompt_template.txt`

Strengthen this section:
```
1. ONLY use SPECIFIC DATA provided above (stores by ID, exact numbers)
```

Add:
```
1. ONLY use SPECIFIC DATA provided above (stores by ID, exact numbers)
2. NEVER say "We should consider" - use "Action: [specific step]"
3. NEVER use generic advice - cite exact store IDs and metrics
```

### Issue: Responses too long

**Fix**: Edit `store_manager_prompt_template.txt`

Add:
```
MAXIMUM: 3 findings, 3 actions, 2 metrics
Each bullet: 1 line maximum
Total response: Under 150 words
```

### Issue: Missing specific insights

**Fix**: Add to `store_manager_metadata_layer.json`

Example:
```json
"your_custom_insight": {
  "description": "Your specific business rule",
  "threshold": "Your specific number",
  "action": "What to do when threshold is hit"
}
```

---

## 📞 Need Help?

1. Read `PROMPT_CUSTOMIZATION_GUIDE.md` for detailed examples
2. Check `store_manager_metadata_layer.json` for all available metadata
3. Look at `COMPLETE_DATA_INSIGHTS.md` for business context

---

**Happy Customizing!** 🎯
