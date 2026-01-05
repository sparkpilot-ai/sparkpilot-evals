# sparkpilot-evals

Test fixtures for Sparkpilot evaluation scenarios.

Each branch contains a specific test scenario with intentional code issues for Sparkpilot to detect.

## Branches

| Branch | Description |
|--------|-------------|
| `scenario/python-bare-except` | Python bare except clause detection |
| `scenario/rust-error-context` | Rust missing error context detection |
| `scenario/rust-unwrap` | Rust unwrap usage detection |
| `scenario/typescript-error-handling` | TypeScript missing error handling |
| `scenario/typescript-floating-promise` | TypeScript floating promise detection |

## Usage

Each scenario branch has two commits:
1. Initial clean code
2. Code with issues to detect

Evals compare `HEAD~1` (base) to `HEAD` (current) to test diff-aware linting.
