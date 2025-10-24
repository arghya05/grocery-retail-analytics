#!/usr/bin/env python3
"""
Grocery Store Manager AI Assistant
Your 24/7 Business Intelligence Partner with 15+ Years Retail Experience
"""

import streamlit as st
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langgraph_multi_agent_store_manager import LangGraphStoreManager

# Page configuration
st.set_page_config(
    page_title="Grocery Store Manager AI",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Retail/Grocery themed
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .business-context {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    .insight-box {
        background-color: #fff8e1;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #ffc107;
    }
    .metric-card {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #4caf50;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'system' not in st.session_state:
    with st.spinner('🔄 Loading Store Manager AI System...'):
        st.session_state.system = LangGraphStoreManager()
    st.success('✅ System Ready!')

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Header
st.markdown('<div class="main-header">🛒 Grocery Store Manager AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your 24/7 AI Business Partner | 15+ Years Retail Experience | Real-Time Data-Driven Insights</div>', unsafe_allow_html=True)

# Business Context Section
st.markdown("""
<div class="business-context">
    <h3>🏪 Your Retail Business at a Glance</h3>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-top: 1rem;">
        <div style="text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #667eea;">50</div>
            <div style="color: #666;">Stores Across 5 Regions</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #667eea;">₹682M</div>
            <div style="color: #666;">Annual Revenue</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #667eea;">1.87M</div>
            <div style="color: #666;">Transactions</div>
        </div>
        <div style="text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: #667eea;">199K</div>
            <div style="color: #666;">Customers</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Key Insights Section
st.markdown("""
<div class="insight-box">
    <h4>💡 Critical Business Insights Available</h4>
    <ul>
        <li><strong>₹304M Revenue Opportunity</strong> identified across 10 initiatives</li>
        <li><strong>₹15-20M Wastage</strong> issue in perishables - actionable solutions ready</li>
        <li><strong>Promotion Problem</strong> reducing ATV by ₹155 - fix strategies available</li>
        <li><strong>Customer Segments</strong> analyzed: Regular, Premium, Occasional, New</li>
        <li><strong>10 Product Categories</strong> with performance metrics and recommendations</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🎯 Quick Actions")

    st.markdown("### 📊 Strategic Questions")
    strategic_questions = [
        "💰 What are the top 3 revenue opportunities?",
        "📈 How can we improve profitability?",
        "🎯 Which customer segment should we prioritize?",
        "🏆 What's our competitive position?",
    ]

    for q in strategic_questions:
        display_text = q
        actual_question = q.split(" ", 1)[1] if " " in q else q
        if st.button(display_text, key=f"strategic_{actual_question}", use_container_width=True):
            st.session_state.current_question = actual_question

    st.markdown("### 🛒 Operational Questions")
    operational_questions = [
        "📦 How can we reduce perishable wastage?",
        "⏰ What's optimal staffing for peak hours?",
        "🚚 How can we improve delivery efficiency?",
        "📊 Which stores need immediate attention?",
    ]

    for q in operational_questions:
        display_text = q
        actual_question = q.split(" ", 1)[1] if " " in q else q
        if st.button(display_text, key=f"operational_{actual_question}", use_container_width=True):
            st.session_state.current_question = actual_question

    st.markdown("### 🛍️ Product & Category Questions")
    product_questions = [
        "🥤 Why is beverage performance strong?",
        "🥬 Which categories have margin opportunity?",
        "📦 How should we optimize product mix?",
        "🏷️ What's causing the promotion problem?",
    ]

    for q in product_questions:
        display_text = q
        actual_question = q.split(" ", 1)[1] if " " in q else q
        if st.button(display_text, key=f"product_{actual_question}", use_container_width=True):
            st.session_state.current_question = actual_question

    st.markdown("---")

    if st.button("🗑️ Clear Chat History", type="secondary", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")

    st.markdown("### 📋 Data Sources Loaded")
    st.markdown("""
    ✅ 20 KPI Datasets (1,151 metrics)
    ✅ Business Intelligence (14 sections)
    ✅ Strategic Insights (975 lines)
    ✅ Multi-Agent Verification System
    """)

    st.markdown("### 🤖 AI Pipeline")
    st.markdown("""
    **Router** → Analyzes Intent
    **Loader** → Fetches Data
    **Analyst** → Store Manager Insights
    **Verifier** → Fact-Checks Numbers
    """)

# Main chat interface
st.markdown("## 💬 Chat with Your Store Manager AI")
st.markdown("*Ask anything about your business - revenue, operations, customers, products, or strategy*")

# Display chat history
if len(st.session_state.chat_history) == 0:
    st.info("👋 Welcome! I'm your AI Store Manager with 15+ years of grocery retail experience. Ask me about revenue opportunities, operational improvements, customer insights, or any business challenge you're facing!")

for chat in st.session_state.chat_history:
    with st.chat_message("user", avatar="👤"):
        st.markdown(f"**You asked:** {chat['question']}")
    with st.chat_message("assistant", avatar="🛒"):
        # Split response into brief and detailed if marker exists
        if "---DETAILED_ANALYSIS_BELOW---" in chat["answer"]:
            parts = chat["answer"].split("---DETAILED_ANALYSIS_BELOW---")
            brief_summary = parts[0].strip()
            detailed_analysis = parts[1].strip() if len(parts) > 1 else ""

            # Show brief summary
            st.markdown(brief_summary)

            # Show detailed analysis in expander
            if detailed_analysis:
                with st.expander("📋 **Click for Detailed Analysis**", expanded=False):
                    st.markdown(detailed_analysis)
        else:
            # Show full answer if no marker
            st.markdown(chat["answer"])

# Chat input box - always visible at bottom
question = st.chat_input("Type your question here... (e.g., 'What are the top revenue opportunities?')", key="chat_input")

# Handle button clicks from sidebar
if 'current_question' in st.session_state:
    question = st.session_state.current_question
    del st.session_state.current_question

# Variable to track if we should process (from either chat input or button)
submit_button = question is not None and len(question.strip()) > 0

# Process question
if submit_button and question:
    # Add to chat history first
    with st.chat_message("user", avatar="👤"):
        st.markdown(f"**You asked:** {question}")

    # Get answer with loading spinner
    with st.chat_message("assistant", avatar="🛒"):
        with st.spinner("🤔 Your Store Manager is analyzing data from 20 KPIs, business intelligence, and strategic insights..."):
            try:
                # Call the LangGraph system
                answer = st.session_state.system.ask(question)

                # Split response into brief summary and detailed analysis
                if "---DETAILED_ANALYSIS_BELOW---" in answer:
                    parts = answer.split("---DETAILED_ANALYSIS_BELOW---")
                    brief_summary = parts[0].strip()
                    detailed_analysis = parts[1].strip() if len(parts) > 1 else ""

                    # Display brief summary first
                    st.markdown(brief_summary)

                    # Add detailed analysis in expander
                    if detailed_analysis:
                        with st.expander("📋 **Click for Detailed Analysis** (Root cause, action plan, execution roadmap)", expanded=False):
                            st.markdown(detailed_analysis)
                else:
                    # Fallback: display full answer if marker not found
                    st.markdown(answer)

                # Add to chat history
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": answer
                })

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.error("Please make sure Ollama is running: `ollama serve`")
                st.info("Need help? Check that Ollama is installed and the llama3.2:1b model is available.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 1rem;">
    <h4 style="color: #667eea; margin-bottom: 1rem;">🛒 Grocery Store Manager AI</h4>
    <p style="font-size: 0.9rem; margin: 0.5rem 0;">
        <strong>Powered by TRUE Multi-Agent Framework</strong><br>
        LangGraph + Ollama + 20 KPI Datasets + Business Intelligence
    </p>
    <p style="font-size: 0.85rem; color: #999; margin-top: 1rem;">
        🔒 100% Private | All data processed locally | No external API calls<br>
        🧠 15+ Years Retail Experience | Real-time fact verification
    </p>
</div>
""", unsafe_allow_html=True)
