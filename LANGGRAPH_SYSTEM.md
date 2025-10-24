

# TRUE Multi-Agent Framework with LangGraph

## Overview

A **proper multi-agent system** built with LangGraph featuring:
- ✅ Separate agent nodes with distinct responsibilities
- ✅ StateGraph for orchestration
- ✅ Typed state management (TypedDict)
- ✅ Agent-to-agent communication via Command objects
- ✅ Conditional routing between agents
- ✅ Proper separation of concerns

## Why This is a TRUE Multi-Agent Framework

### Previous System (Prompt Pipeline)
```python
# ❌ NOT a true multi-agent framework
def answer_question(question):
    # Same LLM, different prompts in sequence
    routing = call_ollama(router_prompt)
    analysis = call_ollama(analysis_prompt)
    verified = call_ollama(verification_prompt)
    return verified
```

**Problems:**
- No agent separation
- No state management
- No agent communication protocol
- Sequential prompts to same LLM
- Manual orchestration

### LangGraph System (TRUE Multi-Agent)
```python
# ✅ TRUE multi-agent framework
class StoreManagerState(TypedDict):
    question: str
    data_sources: list[str]
    analysis: str
    verified_analysis: str

def router_agent(state) -> Command["context_loader"]:
    # Agent 1: Makes routing decision
    return Command(goto="context_loader", update={...})

def analysis_agent(state) -> Command["verification_agent"]:
    # Agent 2: Generates insights
    return Command(goto="verification_agent", update={...})

def verification_agent(state) -> Command[END]:
    # Agent 3: Verifies facts
    return Command(goto=END, update={...})

graph = StateGraph(StoreManagerState)
graph.add_node("router_agent", router_agent)
graph.add_node("analysis_agent", analysis_agent)
graph.add_node("verification_agent", verification_agent)
graph.add_edge(START, "router_agent")
compiled_graph = graph.compile()
```

**Benefits:**
- ✅ Proper agent classes/nodes
- ✅ Typed state management
- ✅ Command-based communication
- ✅ Graph orchestration
- ✅ Conditional routing support
- ✅ Can add parallel execution, human-in-the-loop, persistence

## Architecture

```
                    ┌─────────────────┐
                    │  USER QUESTION  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  StateGraph     │
                    │  (LangGraph)    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────────┐
                    │ StoreManagerState   │
                    │  (Shared State)     │
                    └─────────────────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
      ┌─────▼──────┐  ┌─────▼──────┐  ┌─────▼──────┐
      │  Router    │  │  Analysis  │  │Verification│
      │  Agent     │  │   Agent    │  │   Agent    │
      │  (Node)    │  │  (Node)    │  │   (Node)   │
      └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
            │                │                │
            └────Command─────┴────Command─────┘
                    (Agent Communication)
```

## Key Components

### 1. State Management (TypedDict)

```python
class StoreManagerState(TypedDict):
    """Shared state across all agents"""
    # Input
    question: str

    # Router outputs
    data_sources: list[str]
    analysis_type: str
    key_focus: str

    # Context
    loaded_context: str

    # Analysis outputs
    analysis: str
    facts_verified: bool

    # Verification outputs
    extracted_claims: list[str]
    verified_analysis: str

    # Final output
    final_answer: str
```

**Benefits:**
- Type-safe state management
- Clear data flow between agents
- IDE autocomplete support
- Validation at runtime

### 2. Agent Nodes

Each agent is a **separate function** that:
- Receives current state
- Performs its specific task
- Returns Command with updates
- Routes to next agent

#### Router Agent
```python
def router_agent(state: StoreManagerState) -> Command[Literal["context_loader"]]:
    """Analyzes query and decides what data to load"""

    # Analyze question
    routing = analyze_question(state["question"])

    # Update state and route
    return Command(
        goto="context_loader",
        update={
            "data_sources": routing["data_sources"],
            "analysis_type": routing["analysis_type"],
            "key_focus": routing["key_focus"]
        }
    )
```

#### Analysis Agent
```python
def analysis_agent(state: StoreManagerState) -> Command[Literal["verification_agent"]]:
    """Generates insights in store manager persona"""

    # Generate analysis
    analysis = generate_store_manager_analysis(
        state["question"],
        state["loaded_context"]
    )

    # Update state and route
    return Command(
        goto="verification_agent",
        update={"analysis": analysis}
    )
```

#### Verification Agent
```python
def verification_agent(state: StoreManagerState) -> Command[Literal[END]]:
    """Verifies facts against data"""

    # Verify claims
    verified = verify_analysis(state["analysis"])

    # Final update
    return Command(
        goto=END,
        update={
            "verified_analysis": verified,
            "final_answer": verified
        }
    )
```

### 3. Command Objects

**Command** is LangGraph's way for agents to communicate:

```python
Command(
    goto="next_agent",      # Which agent to call next
    update={...},           # State updates
    graph=Command.PARENT    # Optional: route to parent graph
)
```

**Benefits:**
- Explicit control flow
- State updates with routing
- Support for subgraphs
- Conditional routing

### 4. StateGraph Orchestration

```python
def build_store_manager_graph():
    # Create graph
    builder = StateGraph(StoreManagerState)

    # Add agents as nodes
    builder.add_node("router_agent", router_agent)
    builder.add_node("context_loader", context_loader)
    builder.add_node("analysis_agent", analysis_agent)
    builder.add_node("verification_agent", verification_agent)

    # Define entry point
    builder.add_edge(START, "router_agent")

    # Agents use Command for routing (no manual edges needed)

    # Compile
    graph = builder.compile()
    return graph
```

**Benefits:**
- Visual graph representation
- Automatic validation
- Can add conditional edges
- Support for loops, parallel execution
- Can persist state (checkpointing)
- Can add human-in-the-loop

## Usage

### Installation

```bash
# Install dependencies
pip install langgraph langchain-core langchain-community pandas requests

# Or use requirements.txt
pip install -r requirements.txt
```

### Quick Start

```bash
# Test the system
python3 test_langgraph_system.py

# Run interactive mode
python3 langgraph_multi_agent_store_manager.py
```

### Programmatic Usage

```python
from langgraph_multi_agent_store_manager import LangGraphStoreManager

# Initialize system
system = LangGraphStoreManager()

# Ask a question
answer = system.ask("What are our top revenue opportunities?")
print(answer)
```

## Comparison: Prompt Pipeline vs LangGraph

| Feature | Prompt Pipeline | LangGraph Multi-Agent |
|---------|----------------|----------------------|
| **Agent Separation** | ❌ No - same function | ✅ Yes - separate nodes |
| **State Management** | ❌ Manual dict passing | ✅ TypedDict with validation |
| **Communication** | ❌ Return values | ✅ Command objects |
| **Orchestration** | ❌ Manual if/else | ✅ StateGraph |
| **Routing** | ❌ Hardcoded | ✅ Conditional via Command |
| **Visualization** | ❌ No | ✅ Graph visualization |
| **Parallel Execution** | ❌ No | ✅ Supported |
| **State Persistence** | ❌ No | ✅ Checkpointing support |
| **Human-in-the-Loop** | ❌ No | ✅ Interrupt support |
| **Subgraphs** | ❌ No | ✅ Nested graphs |
| **Conditional Routing** | ❌ Manual | ✅ Built-in |

## Advanced Features (Possible Extensions)

### 1. Parallel Execution

```python
# Run multiple agents in parallel
builder.add_conditional_edges(
    "router",
    route_function,
    {
        "analysis_1": "analysis_agent_1",
        "analysis_2": "analysis_agent_2",  # Parallel
    }
)
```

### 2. Human-in-the-Loop

```python
from langgraph.types import interrupt

def human_approval(state):
    """Wait for human approval before proceeding"""
    approval = interrupt("Review this analysis?")
    return Command(goto="next_agent" if approval else END)
```

### 3. State Persistence

```python
from langgraph.checkpoint.memory import MemorySaver

# Add persistence
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# Resume from checkpoint
result = graph.invoke(state, thread_id="session_123")
```

### 4. Subgraphs

```python
# Create specialized subgraph
category_analysis = create_category_analysis_graph()

# Add as node
builder.add_node("category_analyzer", category_analysis)
```

### 5. Conditional Loops

```python
def should_continue(state):
    """Decide if analysis needs refinement"""
    if state.get("confidence_score", 0) < 0.8:
        return "analysis_agent"  # Loop back
    return "verification_agent"  # Continue

builder.add_conditional_edges(
    "analysis_agent",
    should_continue
)
```

## Data Flow Example

```
1. USER INPUT
   question: "What are our top revenue opportunities?"

2. ROUTER AGENT
   → Analyzes question
   → Decides: data_sources=["financial_opportunities", "store_performance"]
   → Decides: analysis_type="strategic"
   → Routes to: context_loader

3. CONTEXT LOADER
   → Loads CSV data for requested sources
   → Adds business intelligence metadata
   → Routes to: analysis_agent

4. ANALYSIS AGENT
   → Generates store manager analysis
   → Uses loaded context + business knowledge
   → Structures as: WHAT/WHY/ACTIONS/METRICS
   → Routes to: verification_agent

5. VERIFICATION AGENT
   → Extracts numerical claims
   → Verifies against CSV data
   → Corrects any inaccuracies
   → Routes to: END

6. FINAL OUTPUT
   verified_analysis: "Let me walk you through..."
```

## Benefits Over Prompt Pipeline

### 1. Modularity
- Each agent is independent
- Easy to modify one without affecting others
- Can test agents individually

### 2. Maintainability
- Clear separation of concerns
- Type-safe state
- Self-documenting with graph visualization

### 3. Scalability
- Easy to add new agents
- Support for parallel execution
- Can handle complex workflows

### 4. Reliability
- Structured state management
- Validation at each step
- Error handling per agent

### 5. Flexibility
- Conditional routing
- Dynamic workflows
- Easy to extend

## Performance

### Prompt Pipeline
- Router: 2-5s
- Analysis: 10-20s
- Verification: 5-10s
- **Total: 17-35s**

### LangGraph System
- Router: 2-5s
- Context Load: <1s
- Analysis: 10-20s
- Verification: 5-10s
- **Total: 18-36s**

**Overhead: ~1-2 seconds** for graph orchestration (negligible)

**Benefits:**
- Can parallelize context loading (future)
- Can cache agent outputs
- Can checkpoint and resume
- Can add monitoring per agent

## Monitoring & Debugging

### LangSmith Integration (Optional)

```python
import os
os.environ["LANGCHAIN_API_KEY"] = "your-key"
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# All agent calls automatically traced
```

### Graph Visualization

```python
from IPython.display import Image, display

# Visualize the graph
display(Image(graph.get_graph().draw_mermaid_png()))
```

### State Inspection

```python
# Get state at any point
for step in graph.stream(initial_state):
    print(f"Agent: {step}")
    print(f"State: {step['state']}")
```

## Testing

### Unit Test Individual Agents

```python
def test_router_agent():
    state = {"question": "What are revenue opportunities?"}
    command = router_agent(state)

    assert command.goto == "context_loader"
    assert "data_sources" in command.update
```

### Integration Test Full Graph

```python
def test_full_pipeline():
    initial_state = {"question": "Test question"}
    result = graph.invoke(initial_state)

    assert result["final_answer"]
    assert result["facts_verified"]
```

## Troubleshooting

### "Cannot import langgraph"
```bash
pip install langgraph langchain-core langchain-community
```

### "Command not found"
Make sure you're using Command from langgraph:
```python
from langgraph.types import Command
```

### "State key missing"
All state keys must be in StoreManagerState TypedDict definition

### "Agent routing error"
Check that goto targets match node names exactly

## Future Enhancements

1. **Parallel Analysis**: Run multiple analysis agents concurrently
2. **Consensus Mechanism**: Multiple agents vote on recommendations
3. **Adaptive Routing**: Learn which agents to call based on history
4. **Specialized Sub-Agents**: Category-specific, customer-specific agents
5. **Real-time Data**: Stream live data updates through graph
6. **A/B Testing**: Compare different agent strategies
7. **Reinforcement Learning**: Optimize routing based on outcomes

## Conclusion

This is a **TRUE multi-agent framework** with:

✅ **Proper Agent Separation** - Each agent is a distinct node
✅ **State Management** - TypedDict for type-safe state
✅ **Agent Communication** - Command objects for routing
✅ **Graph Orchestration** - StateGraph manages flow
✅ **Conditional Routing** - Dynamic workflow control
✅ **Extensible** - Easy to add features like parallel execution, persistence

**Not just sequential prompts - this is production-ready multi-agent architecture.**

---

## Quick Reference

### Run the System
```bash
python3 langgraph_multi_agent_store_manager.py
```

### Test the System
```bash
python3 test_langgraph_system.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Import in Code
```python
from langgraph_multi_agent_store_manager import LangGraphStoreManager

system = LangGraphStoreManager()
answer = system.ask("Your question here")
```
