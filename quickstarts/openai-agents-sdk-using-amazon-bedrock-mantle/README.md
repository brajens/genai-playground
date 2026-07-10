# OpenAI Agents SDK with AWS Bedrock Mantle - Quickstart Tutorial

A comprehensive tutorial for building AI agents using the OpenAI Agents SDK with AWS Bedrock Mantle endpoints.

## Attribution

This tutorial is based on code examples and patterns from the [OpenAI Agents Python documentation](https://openai.github.io/openai-agents-python/agents/). The examples have been adapted to work with AWS Bedrock Mantle endpoints. All credit for the core SDK design and examples goes to OpenAI.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Tutorial Sections](#tutorial-sections)
- [Learning Paths](#learning-paths)
- [Reference](#reference)

## Introduction

This tutorial teaches you how to build AI agents using the OpenAI Agents SDK integrated with AWS Bedrock Mantle. You'll learn:

- Creating and orchestrating AI agents
- Building tools and multi-agent workflows
- Managing conversation state and streaming responses
- Implementing safety guardrails and human-in-the-loop patterns
- Integrating with Model Context Protocol (MCP) tools
- Monitoring and observability

**What is AWS Bedrock Mantle?**
AWS Bedrock Mantle provides OpenAI-compatible API endpoints for models hosted on AWS Bedrock, allowing you to use the OpenAI Agents SDK with AWS-managed models.

## Prerequisites

### Installation

```bash
pip install openai openai-agents aws-bedrock-token-generator
```

### Authentication Setup

All notebooks use this standard authentication pattern:

```python
from openai import AsyncOpenAI
from agents import (
    set_default_openai_client,
    set_default_openai_api,
    set_tracing_disabled,
)
from aws_bedrock_token_generator import provide_token

client = AsyncOpenAI(
    api_key=provide_token(),
    base_url="https://bedrock-mantle.us-east-1.api.aws/openai/v1",
    project="default"
)

set_default_openai_client(client)
set_default_openai_api("responses")
set_tracing_disabled(True)  # OpenAI-platform tracing can't reach Mantle
```

**Model ID Convention**: Use `"openai.gpt-5.5"` as the Mantle model identifier.

## Quick Start

### Your First Agent

```python
from agents import Agent, Runner

agent = Agent(
    name="History tutor",
    instructions="You answer history questions clearly and concisely.",
    model="openai.gpt-5.5"
)

result = await Runner.run(agent, "When did the Roman Empire fall?")
print(result.final_output)
```

## Tutorial Sections

### 1. Fundamentals

Learn the core concepts of the OpenAI Agents SDK.

| Notebook | Description | Key Concepts |
|----------|-------------|--------------|
| [basic-agent.ipynb](01-fundamentals/basic-agent.ipynb) | Create your first agent | Agent creation, Runner execution |
| [tools.ipynb](01-fundamentals/tools.ipynb) | Add function tools to agents | @function_tool decorator, tool integration |
| [structured-output.ipynb](01-fundamentals/structured-output.ipynb) | Type-safe responses | Pydantic models, output_type parameter |
| [streaming.ipynb](01-fundamentals/streaming.ipynb) | Real-time token streaming | Runner.run_streamed(), ResponseTextDeltaEvent |


### 2. Multi-Agent Systems

Build sophisticated agent orchestration patterns.

| Notebook | Description | Key Concepts |
|----------|-------------|--------------|
| [handoffs.ipynb](02-multi-agent/handoffs.ipynb) | Route between specialist agents | handoff_description, routing logic |
| [agents-as-tools.ipynb](02-multi-agent/agents-as-tools.ipynb) | Convert agents to callable tools | .as_tool() method, explicit invocation |
| [handoff-callbacks.ipynb](02-multi-agent/handoff-callbacks.ipynb) | Lifecycle hooks for handoffs | on_handoff callbacks, audit logging |


### 3. Advanced Tools

Master tool configuration and execution patterns.

| Notebook | Description | Key Concepts |
|----------|-------------|--------------|
| [tool-configuration.ipynb](03-advanced-tools/tool-configuration.ipynb) | Control tool invocation | ModelSettings, tool_choice, tool_use_behavior |
| [tool-execution.ipynb](03-advanced-tools/tool-execution.ipynb) | Files, timeouts, error handling | ToolOutputFileContent, timeout parameter, failure_error_function |
| [human-approval.ipynb](03-advanced-tools/human-approval.ipynb) | Require approval for sensitive operations | needs_approval, interruptions, state management |
| [conditional-tools.ipynb](03-advanced-tools/conditional-tools.ipynb) | Context-based tool availability | is_enabled predicate, dynamic tool selection |


### 4. Configuration

Customize agent behavior and lifecycle.

| Notebook | Description | Key Concepts |
|----------|-------------|--------------|
| [model-settings.ipynb](04-configuration/model-settings.ipynb) | Reasoning effort and verbosity | ModelSettings, reasoning levels, verbosity control |
| [dynamic-instructions.ipynb](04-configuration/dynamic-instructions.ipynb) | Context-aware instructions | RunContextWrapper, dynamic instruction generation |
| [lifecycle-hooks.ipynb](04-configuration/lifecycle-hooks.ipynb) | Monitor agent execution | RunHooks, on_agent_start, on_llm_end, on_agent_end |


### 5. State Management

Handle multi-turn conversations and error scenarios.

| Notebook | Description | Key Concepts |
|----------|-------------|--------------|
| [conversation-state.ipynb](05-state-management/conversation-state.ipynb) | Three approaches to conversation state | input_list (stateless), SQLiteSession (persistent), response_id (server-side) |
| [error-handling.ipynb](05-state-management/error-handling.ipynb) | Global error handling strategies | RunErrorHandlerInput, custom error messages |


### 6. Safety & Guardrails

Implement comprehensive safety systems.

| Notebook | Description | Key Concepts |
|----------|-------------|--------------|
| [guardrails.ipynb](06-safety-guardrails/guardrails.ipynb) | Multi-layer safety system | @input_guardrail, @tool_input_guardrail, @tool_output_guardrail, @output_guardrail |


### 7. MCP Integration

Connect to external services via Model Context Protocol.

| Notebook | Description | Key Concepts |
|----------|-------------|--------------|
| [using-mcp-servers.ipynb](07-mcp-integration/using-mcp-servers.ipynb) | Integrate MCP-hosted tools | HostedMCPTool, connector_id, AWS ARNs |Stream responses with MCP tools


### 8. Observability

Monitor, track, and visualize agent behavior.

| Notebook | Description | Key Concepts |
|----------|-------------|--------------|
| [usage-tracking.ipynb](08-observability/usage-tracking.ipynb) | Monitor token consumption | result.context_wrapper.usage, cost tracking |
| [visualization.ipynb](08-observability/visualization.ipynb) | Visualize agent architectures | draw_graph(), agent diagrams |


## Learning Paths

### Beginner Path (2-3 hours)

Perfect for developers new to AI agents:

1. **Fundamentals** (all 3 notebooks)
   - Start with `basic-agent.ipynb`
   - Add tools with `tools.ipynb`
   - Structured outputs with `structured-output.ipynb`
   - Streaming output with `streaming.ipynb`

2. **Multi-Agent Basics**
   - Agent handoffs with `handoffs.ipynb`

3. **First Project**: Build a simple multi-agent customer support system

### Intermediate Path (4-6 hours)

For developers with basic agent knowledge:

1. **Advanced Tools** (all 4 notebooks)
   - Tool configuration and execution patterns
   - Human approval workflows

2. **Configuration** (all 3 notebooks)
   - Model settings and dynamic instructions
   - Lifecycle monitoring

3. **State Management** (both notebooks)
   - Choose your conversation state approach

4. **Second Project**: Build a stateful agent with custom tools and approval workflows

### Advanced Path (6-8 hours)

For experienced practitioners:

1. **Safety** 
   - Complete guardrails system

2. **MCP Integration** (both notebooks)
   - External service integration

3. **Observability** (all 3 notebooks)
   - Monitoring and visualization

4. **Advanced Project**: Production-ready multi-agent system with safety, MCP tools, and monitoring

## Reference

### Common Patterns

#### Agent Creation
```python
agent = Agent(
    name="Agent Name",
    instructions="Clear, specific instructions",
    model="openai.gpt-5.5",
    tools=[...],  # Optional
    output_type=YourModel,  # Optional, for structured output
)
```

#### Running Agents
```python
# Basic execution
result = await Runner.run(agent, "user input")

# With session (persistent state)
result = await Runner.run(agent, "user input", session=session)

# Streaming
result = Runner.run_streamed(agent, "user input")
async for event in result.stream_events():
    # Process events
```

#### Tool Definition
```python
@function_tool
def your_tool(param: str) -> str:
    """Tool description for the model."""
    return "result"

# With options
@function_tool(
    timeout=5.0,
    needs_approval=True,
    failure_error_function=custom_error_handler
)
def sensitive_tool(data: str) -> str:
    return "result"
```

### Model Settings

```python
from agents import ModelSettings
from openai.types.shared import Reasoning

settings = ModelSettings(
    reasoning=Reasoning(effort="low"),  # low, medium, high
    verbosity="low",  # low, medium, high
    tool_choice="auto"  # auto, required, none, or "tool_name"
)

agent = Agent(..., model_settings=settings)
```

### Best Practices

1. **Clear Instructions**: Be specific about what the agent should do
2. **Tool Descriptions**: Write clear docstrings - the model reads them
3. **Error Handling**: Use custom error functions for user-friendly messages
4. **State Management**: Choose based on your needs:
   - `input_list`: Full control, stateless
   - `SQLiteSession`: Automatic persistence
   - `response_id`: Simple server-side state
5. **Guardrails**: Layer them (input → tool → output) for comprehensive safety
6. **Testing**: Test multi-agent flows with various inputs

### Troubleshooting

**Issue**: Agent not using tools
- Check tool descriptions are clear
- Verify `tool_choice` setting
- Ensure instructions mention when to use tools

**Issue**: Conversation loses context
- Verify you're using state management (session, input_list, or response_id)
- Check that context is passed correctly between turns

**Issue**: Timeouts or slow responses
- Adjust `timeout` parameter on tools
- Consider `reasoning` effort level
- Check for long-running tool operations

**Issue**: MCP tools not working
- Verify connector_id ARN is correct
- Check `require_approval` setting
- Ensure `allowed_tools` list includes the tool

## Additional Resources

- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents-python)
- [AWS Bedrock Mantle Documentation](https://docs.aws.amazon.com/bedrock/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/) (for structured outputs)

## Repository Structure

```
quickstart/
├── README.md                      # This file
├── 01-fundamentals/              # Core concepts
├── 02-multi-agent/               # Agent orchestration
├── 03-advanced-tools/            # Tool patterns
├── 04-configuration/             # Agent customization
├── 05-state-management/          # Conversation state
├── 06-safety-guardrails/         # Safety systems
├── 07-mcp-integration/           # External services
└── 08-observability/             # Monitoring and viz
```

## Contributing

Found an issue or have a suggestion? Please open an issue or submit a pull request.

## License

[Your License Here]
