# Operations

## Ownership

- Service owner: Web app maintainers for django-polls-portal.

## Monitoring

- Track poll publication rate, response throughput, and submission error rates.
- Track retention cleanup command outcomes and failures.

## Rollback

- Disable publish endpoint if severe defects occur.
- Preserve existing records while rollback is performed.

## Tags

- Environment, repository, owner, and service tags should be set via IaC.
