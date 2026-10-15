# Roadmap

**incident-agent** is an AI agent that autonomously investigates production incidents.

A small microservices environment (the *lab*) runs under constant load. A chaos scenario injects a fault (a slow database, a memory leak, a bad config, a crashing service). An alert fires, and the agent investigates on its own: it reads logs, queries metrics, inspects containers and recent commits, then writes a root-cause report with a suggested fix. An evaluation harness compares each report to the known ground truth and measures accuracy, time and cost.

## Architecture

```
incident-agent/
├── lab/            # The environment under test
│   ├── services/       # gateway → orders → payments (FastAPI)
│   ├── loadgen/        # Continuous traffic generator
│   └── docker-compose.yml   # + Postgres, Redis, Prometheus, Loki, Grafana
├── chaos/          # Fault injection
│   └── scenarios/      # One YAML per fault: how to inject it + the ground-truth root cause
├── agent/          # The investigation agent
│   ├── loop.py         # Hand-written agent loop (Claude API, tool use)
│   ├── tools/          # query_logs, query_metrics, list_containers, inspect_container, git_log, read_file
│   └── report.py       # Structured report: root cause, evidence, fix, confidence
├── mcp_server/     # The same tools exposed over MCP, usable from any MCP client
├── eval/           # Evaluation harness: reset → inject → investigate → grade
└── ui/             # Live view of an investigation
```

## Milestones

### 1. The lab: services and observability
- [x] `orders` service: REST API (FastAPI, Pydantic), structured JSON logs
- [x] Containerized with Docker and Docker Compose
- [x] Orders persisted in Postgres (SQLAlchemy)
- [ ] `payments` service, called by `orders`
- [ ] `gateway` service as the single entry point
- [ ] Metrics with Prometheus, logs with Loki, dashboards with Grafana
- [ ] Load generator for continuous traffic

### 2. Chaos scenarios and alerting
- [ ] Scenario format (YAML) with injection steps and ground-truth root cause
- [ ] First 3 scenarios (e.g. exhausted database connection pool, crashing service, injected latency)
- [ ] CLI to inject and revert a scenario
- [ ] Prometheus alert rules that fire when a fault is injected

### 3. Agent v0
- [ ] Agent loop written from scratch on the Claude API (no agent framework)
- [ ] First tools: logs, metrics, containers
- [ ] Output truncation and guardrails (read-only tools, sandboxed execution)
- [ ] Structured root-cause report
- [ ] The agent finds the root cause of at least one scenario on its own

### 4. Evaluation harness
- [ ] Automated runs: reset the lab → inject → investigate → grade
- [ ] Grading against ground truth (exact category match + LLM judge for the explanation)
- [ ] Metrics: accuracy, time to root cause, cost per investigation
- [ ] First published score

### 5. Scale and improve
- [ ] 15–20 scenarios
- [ ] Agent improvements (prompting, planning, context management), measured against the eval
- [ ] MCP server exposing the investigation tools
- [ ] Comparison across models and settings

### 6. Visibility
- [ ] Web UI streaming an investigation live
- [ ] Tracing of every agent step (tool calls, tokens, latency)
- [ ] Cost tracking per investigation

### 7. Production quality
- [ ] Unit and integration tests
- [ ] CI with GitHub Actions
- [ ] README with architecture diagram, results and limitations
- [ ] 2-minute demo video

## Design principles

- **Measure everything.** Every change to the agent is judged by the eval score, not by impressions.
- **Own the agent loop.** The loop, tools and context management are written by hand, to keep full control and understanding of how the agent behaves.
- **Safe by default.** Investigation tools are read-only and the agent runs with strict limits.
- **Cost-aware.** Prompt caching, truncated tool output, and the cheapest model that holds quality for each task.
