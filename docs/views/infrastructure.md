# infrastructure view

an installation may combine a durable server, a personal computer, a browser
profile and a phone. choose hosts by the capability needed for the outcome.
public web reads need not depend on a logged-in personal desktop. a personal
session or local device requires its actual authorized host.

## keep these layers separate

source revision → release artifact → installed files → actual launcher → running
process → authorized invocation → fresh source → verified human outcome.

a matching git head covers one layer. it does not back up private task databases,
sessions, media or in-memory state. use separate installation-local backup and
restore receipts for those resources.

## release and recovery

1. identify consumers, source versions and the currently working route.
2. prepare an isolated versioned artifact and retain a verified rollback.
3. validate source and packaging without changing the service environment.
4. update the intended consumer through its normal launcher.
5. verify an actual authorized operation and independent readback.
6. test restart, reconnect and a cold start when unattended use requires it.

source-only success is `source_checked`. do not close a consumer release from a
green worker process. preserve unknown effects and pending tasks during rollback.

## credentials and local state

use an installation-owned scoped credential runtime, process-scoped injection
and provider-owned sessions. commit reference templates, never resolved values.
reuse the established launcher and encrypted recovery mechanism rather than
building per-project secret caches. a credential rotation is a consumer migration:
update saved clients and verify a real consumer, not only the secret store.

## observe with proportionate cost

use deterministic source reads, cursors and change detection while waiting.
start reasoning when evidence requires a decision. retries, model budgets and
notification policy are separate controls. bound provider backoff and retain an
armed continuation. a written “check later” is not a working wake-up mechanism.

## source synchronization

inventory all registered worktrees and installed source projections. compare
against fresh remote heads, then check patch equivalence before declaring code
missing. preserve reviewed work on isolated branches. reconcile divergent versions
through scoped changes and tests. verify the remote sha after push. recover files
from their actual host. an absent server snapshot does not establish absence on
the source computer.
