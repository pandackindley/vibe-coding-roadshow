# Copilot Instructions for vibe-coding-roadshow

## Overview
This repository contains multiple projects and frameworks for collaborative GenAI, DevOps, and game/web applications. Key subprojects include:
- `django-cpe-tracker/`: Django app for tracking CPE experiences
- `go-mastermind-webapp/`: Go webapp for Mastermind game
- `genai-collaboration/`: GenAI DevOps guard rail framework and standards
- `ror-connect4/`: (Ruby on Rails, details not expanded)

## Architecture & Major Components
- **GenAI Collaboration Framework**: Located in `genai-collaboration/`, this directory provides guard rails, standards, and collaborative workflows for integrating AI agents into DevOps. Key files:
  - `alignment-framework/`: Contains project/session guard rails, guardian loop, self-improvement docs
  - `community-constraint-library/`: Versioned manifests for coding standards (Python, YAML, Terraform, SRE, etc.)
  - `README.md`: Entry point for framework usage and onboarding
- **Django CPE Tracker**: Standard Django structure. Key files:
  - `manage.py`, `cpe_tracker/settings.py`, `credits/models.py`, `credits/views.py`
  - Custom templates in `credits/templates/credits/`
  - Static assets in `credits/static/credits/`
- **Go Mastermind Webapp**: Contains Go source and test files. See `main.go`, `main_test.go`, and documentation files for rules and technical overview.

## Developer Workflows
- **Linting**: All markdown and code files must be lint-compliant. See manifests in `community-constraint-library/` for language-specific standards.
- **Testing**:
  - Django: Use `python manage.py test` in `django-cpe-tracker/`
  - Go: Use `go test` in `go-mastermind-webapp/`
- **Documentation**: All standards and guard rails are referenced, not copied. Always use canonical sources in `genai-collaboration/community-constraint-library/`.
- **Change Logging**: Manual and automated changes should be logged per commit, distinguishing agent vs. user actions.

## Project-Specific Patterns
- **Guard Rails Enforcement**: Agents must self-audit outputs for compliance with project and session guard rails before presenting results. See `alignment-framework/project_guard_rails.md` and `alignment-framework/session_guard_rails.md`.
- **Collaborative Review**: Use the Guardian Loop (`alignment-framework/guardian_loop.md`) for real-time mentoring and approval.
- **Self-Improvement**: Agents should periodically review and suggest improvements to guard rails and workflow (`alignment-framework/self_improvement.md`).
- **Reference Management**: Audit documentation for outdated references; remove links to deleted files immediately.

## Integration Points
- **External Standards**: Reference manifests in `community-constraint-library/` for Python, YAML, Terraform, SRE, and AI collaboration.
- **Templates & Static Assets**: Django templates and static files are organized under `credits/templates/credits/` and `credits/static/credits/`.

## Examples
- To add a new coding standard, place the manifest in `community-constraint-library/` and link it in the main `README.md`.
- To update guard rails, edit the relevant file in `alignment-framework/` and ensure all contributors are notified.

## Key References
- `genai-collaboration/README.md`: Framework entry point
- `genai-collaboration/alignment-framework/project_guard_rails.md`: Universal guard rails
- `genai-collaboration/alignment-framework/session_guard_rails.md`: Session-specific guard rails
- `genai-collaboration/alignment-framework/guardian_loop.md`: Collaborative review workflow
- `genai-collaboration/alignment-framework/self_improvement.md`: Agent self-improvement
- `genai-collaboration/community-constraint-library/`: Coding standards manifests

---
For questions or feedback, see `genai-collaboration/howto/HOWTO_README.md` and contact the project maintainer as described there.
