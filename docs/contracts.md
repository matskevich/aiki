# cross-component contracts

these are portable documentation contracts and synthetic examples. actual runtime
schemas are owned by their providers. an adopter must map these concepts to the
real schema instead of sending an example directly to a service.

| record | minimum meaning |
| --- | --- |
| capability | stable id, effect, resource/host, schema revision and dated evidence |
| task | goal, authority source, intent revision, accountable owner and acceptance |
| operation | idempotency key, exact target, dispatch state and effect receipt |
| stage handoff | parent identity, facts, effects, uncertain operations and next decision |
| observation | source, event time, observed time, coverage, freshness and cursor |
| owner input | exact task/input/revision, question, blocked action and resolution |
| acceptance | source, artifact, consumer, actual operation, independent result and limits |

unknown is an information state, not proof that nothing happened. keep a dispatched
operation's identity across retries. a lease controls execution coordination,
not authority or proof that a remote process has stopped.

## sources and projections

the task coordinator owns task state. a domain project owns substantive decisions
and artifacts. a provider owns its sessions and domain action rules. a projection
owns mappings and delivery receipts. declare any exceptions in the installation.

one record can reference another without importing its private contents. public
examples use synthetic identifiers and `example.invalid` urls.

examples: [task](../examples/task.json), [handoff](../examples/handoff.json),
[acceptance](../examples/acceptance.json).
