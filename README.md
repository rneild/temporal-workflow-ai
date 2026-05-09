# Temporal Workflows

> Managed by ATB (Agentic Temporal Builder). Each workflow runs as an AWS Lambda worker connected to Temporal Cloud.

## Deployed Workflows

| Name | ID | Trigger | Task Queue | Intent |
|------|----|---------|------------|--------|
| [hello-world](hello-world-fbb969/) | `hello-world-fbb969` | adhoc | `tq-hello-world-fbb969` | [INTENT.md](hello-world-fbb969/INTENT.md) |
| [perfect_cup_of_coffee](perfect_cup_of_coffee-83eb42/) | `perfect_cup_of_coffee-83eb42` | adhoc | `tq-perfect_cup_of_coffee-83eb42` | [INTENT.md](perfect_cup_of_coffee-83eb42/INTENT.md) |
| [simple-greeter](simple-greeter-324664/) | `simple-greeter-324664` | adhoc | `tq-simple-greeter-324664` | [INTENT.md](simple-greeter-324664/INTENT.md) |

## Workflow Structure

Each directory contains:

- `workflow.py` — Temporal workflow definition
- `activities.py` — Activity implementations
- `worker.py` — Lambda worker entry point
- `requirements.txt` — Python dependencies
- `tests/test_workflow.py` — Test suite
- `INTENT.md` — Design intent, key decisions, and change history
