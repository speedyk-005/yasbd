# Contributing to yasbd: Technician & Calibration Manual

The maintenance bench is open. Grab your protective eyewear, pick up your calipers, and let's calibrate some high-speed sentence shearing equipment.

We don't do sloppy hacks or blunt tears here. yasbd is a zero-copy, low-memory, rule-based boundary shearing unit. If you are here to modify the cutting edge, you must adhere to the strict mechanical tolerances outlined in this manual.

## Bench Setup

Before you touch the live micro-blades, you need to set up an isolated diagnostic environment.

### Clone the Blueprint

Pull the official schematics from the main repository:

```bash
git clone https://github.com/speedyk-005/yasbd-lib.git
cd yasbd-lib
```

### Calibrate the Environment

Create and activate your virtual environment by running python -m venv. Do not install dependencies globally unless you enjoy contaminating your workshop.

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Install the Tooling

Install the development package with the necessary testing rigs using pip.

```bash
pip install -e ".[dev]"

# Optional: only needed for some components
pip install spacy -U
pip install langcodes -U
```

## Making Modifications

Do not make adjustments directly to the main production line. Work on an isolated branch.

### Create a Branch

Use a standardized prefix so the telemetry system knows what you are touching:

```bash
# For mechanical upgrades:
git checkout -b feature/my-feature-branch

# For structural repairs:
git checkout -b bugfix/issue-number-description
```

### Add a New Language Module

Copy [`src/yasbd/rules/_template.py`](src/yasbd/rules/_template.py) to `src/yasbd/rules/{lang}.py`, rename the class to `{Lang}Rules`, fill in the sets your language needs, and add test data to `tests/test_data/{lang}.py`. Auto-discovered at runtime, no registration needed.

### Run Diagnostics

If you change the teeth of a blade, you must verify it still cuts straight. Run the test suite using pytest:

```bash
# All
pytest

# For a single language only, use the `-k` filter:
pytest tests/test_boundary_detector.py -k "test_segment_multiple_langs and pl-"
```

### Machine the Surfaces

Our code surfaces must be perfectly smooth. Before pushing, sand down the rough edges:

```bash
ruff format && ruff check --fix
```

If you modified any set literals in rule files (abbreviation sets, section markers, etc.),
reformat them for consistent line widths:

```bash
python3 scripts/reformat_sets.py
```

Pre-commit hooks are available to automate this. Install them with:

```bash
pre-commit install
```

This runs `ruff` on every commit so you never forget.

### Build Documentation

If you changed any docstrings or public interfaces, regenerate the docs:

```bash

# Generate API_REFERENCES.md from docstrings
bash scripts/gen_api_docs.sh
```

## Quality Guidelines

### Component Ordering

To keep the machinery readable for other technicians, arrange class components bottom-up, fundamentals first, public interface last:

1. Class docstring (describes what the machine does)
2. Constants and static configuration attributes
3. Constructor (`__init__`)
4. Read-only instrumentation properties (`@property`)
5. Private helper components (`_private_method`)
6. Public operational controls (`public_method`)

```python
class ExampleClass:
    """Detailed structural docstring explaining the component's purpose."""

    STATIC_TOLERANCE_BOUND = 0.005

    def __init__(self):
        """Prepares internal state and registers caching arrays."""
        self._value = None

    @property
    def current_tolerance(self):
        """Exposes raw tracking metrics to downstream monitors."""
        return self._value

    def _execute_lookahead(self):
        """Low-level scan step. No docstring needed unless it gets weird."""
        pass

    def execute_split(self):
        """Triggers the primary physical slice on the input text stream."""
        pass
```

### Docstring Standards

All public interface controls must be documented using Google-style docstrings. Explain your arguments, return types, and exceptions clearly. If your code is too complex for a standard docstring, simplify your logic or document the mathematical assumptions clearly.

## Pull Request Template

A few rules keep the review queue running smoothly:

- Keep no more than three pull requests open at once. If you are at the limit, merge one before opening the next. A pile of unmerged branches only gums up the queue and drags out reviews.
- A PR that has been reviewed and then sits unfixed for weeks may be closed or superseded. Review comments are a request for action, not a suggestion. If you cannot get back to it promptly, say so, and we will decide whether to close it or hand it to someone else.
- If multiple pull requests address the same issue, we evaluate them based on code quality and test coverage. If the implementations are structurally identical, we merge the earliest submission.
- Use the [PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) when submitting.
- Include a row for yourself in [CONTRIBUTORS.md](CONTRIBUTORS.md) in the same PR that contains your contribution: your GitHub handle and a short note on what you did. Already on the list? Update your existing row instead of adding a duplicate.
- Prefer extending existing test files and doctests over adding new test files. A new test file for a small change adds review overhead and fragments coverage; add cases to the tests that already cover the module instead.
- Start PR branches from a clean `main`, not from a branch that carries changes from past edits or other PRs. A branch polluted with unrelated commits makes the diff noisy and hard to review.

## Conduct

We are adults here trying to build high-performance software. Be civil, respect different architectural opinions, and remember that behind every GitHub profile is a human being who probably has better things to do than argue over irrelevant formatting details.

If you cannot cooperate on the workshop floor without making the experience miserable or hostile for other technicians, please pack up your tools and find a different project to work on. We are here to ship fast code, not to psychoanalyze each other's lifestyle choices. Keep your communication professional, direct, and constructive, and the machinery will run perfectly.
