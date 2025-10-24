# Store Manager Prompt Customization Guide

## Overview

The Store Manager AI prompt is now stored in an external file for easy customization:

**File**: `store_manager_prompt_template.txt`

## How to Customize

1. **Open the file**:
   ```bash
   nano store_manager_prompt_template.txt
   # or use any text editor
   ```

2. **Edit any section** you want to change:
   - Change the persona/role
   - Modify response format
   - Add/remove emojis
   - Change tone and style
   - Adjust formatting rules
   - Update examples

3. **Save the file**

4. **Restart the app** - Changes take effect immediately:
   ```bash
   streamlit run store_manager_app.py
   ```

## Template Variables

The template uses these dynamic variables (DO NOT remove):

- `{expertise_context}` - Injected domain knowledge based on question type
- `{data_context}` - Actual data from CSV files
- `{question}` - User's question

## Customization Examples

### Example 1: Change Response Format

**Original**:
```
**📊 KEY FINDINGS**
• [bullet point]

**🎯 IMMEDIATE ACTIONS**
1. [action]
```

**Customized** (More sections):
```
**📊 KEY FINDINGS**
• [bullet point]

**🔍 ROOT CAUSE**
• [analysis]

**🎯 IMMEDIATE ACTIONS**
1. [action]

**💰 FINANCIAL IMPACT**
• [impact]
```

### Example 2: Change Tone

**Original**:
```
3. Store managers are BUSY - get to the point fast
```

**Customized** (More detailed):
```
3. Provide detailed analysis with context and reasoning
```

### Example 3: Add New Section

Add after TRACK DAILY/WEEKLY:
```
**🔮 NEXT 30 DAYS** (Strategic Plan)
• Week 1: [milestone]
• Week 2: [milestone]
• Week 3: [milestone]
• Week 4: [milestone]
```

### Example 4: Change Emojis

**Original**:
```
=== EMOJIS TO USE ===
📊 Data/Findings | 🎯 Actions | 📈 Metrics | ⚠️ Critical Issues | 💡 Insights
```

**Customized** (Professional):
```
=== EMOJIS TO USE ===
▶️ Data/Findings | ✓ Actions | → Metrics | ! Critical Issues | • Insights
```

### Example 5: Add Industry-Specific Language

Add a new section:
```
=== INDUSTRY-SPECIFIC TERMS ===
• Always mention "Same Store Sales" (SSS) for comparisons
• Reference "Category Captain" for top-performing categories
• Use "Planogram compliance" when discussing shelf management
• Mention "Loss leader" for strategic pricing
```

## Popular Customizations

### 1. More Detailed Responses

Change:
```
2. Be BRIEF and use BULLET POINTS
```

To:
```
2. Provide comprehensive analysis with supporting details
```

### 2. Focus on Specific Metrics

Add:
```
=== ALWAYS INCLUDE ===
• Gross margin impact
• Labor cost implications
• Customer satisfaction effect
• Inventory turnover
```

### 3. Add Risk Assessment

Add a new section to format:
```
**⚠️ RISKS & MITIGATION**
• Risk 1: [description] → Mitigation: [action]
• Risk 2: [description] → Mitigation: [action]
```

### 4. Include Competitive Benchmarks

Add:
```
**🏆 VS INDUSTRY BENCHMARK**
• Your metric: [value] | Industry avg: [value] | Gap: [%]
```

## Advanced Customization

### Multi-Language Support

Create language-specific templates:
- `store_manager_prompt_template_en.txt` (English)
- `store_manager_prompt_template_hi.txt` (Hindi)
- `store_manager_prompt_template_es.txt` (Spanish)

Update code to load based on preference.

### Role-Based Templates

Create different templates for different roles:
- `store_manager_prompt_template.txt` (Default)
- `regional_manager_prompt_template.txt` (Regional view)
- `ceo_prompt_template.txt` (Executive summary)

### Question-Type Templates

Create specialized templates:
- `prompt_revenue_analysis.txt`
- `prompt_customer_insights.txt`
- `prompt_operational_issues.txt`

## Testing Your Changes

1. **Make a small change** first (e.g., add an emoji)
2. **Restart the app**
3. **Ask a test question**: "What are the top 5 stores?"
4. **Verify** the output matches your expectations
5. **Iterate** until satisfied

## Best Practices

✅ **DO**:
- Test changes incrementally
- Keep the template variables intact
- Maintain clear formatting
- Document your changes
- Back up original template

❌ **DON'T**:
- Remove `{expertise_context}`, `{data_context}`, or `{question}`
- Make the prompt too long (LLM context limits)
- Remove critical instructions about using specific data
- Add contradictory instructions

## Backup Original

Before major changes:
```bash
cp store_manager_prompt_template.txt store_manager_prompt_template.backup.txt
```

## Restore Original

If something breaks:
```bash
cp store_manager_prompt_template.backup.txt store_manager_prompt_template.txt
```

## Troubleshooting

### Issue: Responses are too generic

**Fix**: Add this to CRITICAL INSTRUCTIONS:
```
5. NEVER use phrases like "We should" or "Consider" - be DIRECTIVE
```

### Issue: Responses are too long

**Fix**: Add:
```
Maximum response: 200 words
Each bullet: 1 line maximum
```

### Issue: Missing specific data

**Fix**: Strengthen this rule:
```
1. ONLY use SPECIFIC DATA provided above - NEVER invent numbers
2. If data is missing, say "Data not available" instead of guessing
```

### Issue: Wrong format

**Fix**: Add examples showing exact format:
```
=== EXACT FORMAT EXAMPLE ===
[Paste your desired output format here]
```

## Support

If you need help:
1. Check the examples in this guide
2. Review the default template
3. Test with simple questions first
4. Verify template variables are preserved

## Version History

- **v1.0** (Current): Brief, bullet-point format for busy store managers
- **v0.9**: Detailed, paragraph format (legacy)

---

**Happy Customizing!** 🛒📝
