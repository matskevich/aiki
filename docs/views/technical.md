# technical view

| abstraction | responsibility | state it owns |
| --- | --- | --- |
| agent client | expose available tools and execute the reasoning session | client/session context |
| skill | guide decisions and retrieval | reusable instructions, no action grant |
| context source | retrieve source-backed facts and domain state | private records and provenance |
| capability catalog | describe resources, operations, schemas and routes | versioned metadata, grants where implemented |
| connector | present a service interface to the client | transport configuration and bindings |
| provider | interact with an account/system and enforce domain rules | provider sessions, limits and operation receipts |
| task coordinator | retain goal, authority, effects and continuation | canonical task and stage state |
| device stage | execute an outcome requiring its host | bounded execution and checkpoint |
| watch | observe a source and resume work on meaningful change | cursor, matcher and next check |
| projection | display canonical state in another surface | mapping and projection receipt |
| domain application | own substantive content and decisions | domain case or artifact |

mcp is one interface protocol. a plugin packages a client entry point. neither
implies a particular reasoning model, hosted service or permission level.

## composition

preserve task identity, operation identity, intent revision, authority source,
state owner and observed effects at each handoff. see [contracts](../contracts.md).
explicitly distinguish required dependencies from optional integrations.

the coordinator should remain accountable while a device stage works. before
retrying after a disconnect, inspect the prior operation and remote executor.
lease expiry does not prove that the remote process stopped.

linear, chat topics and dashboards can project canonical task state. define the
direction of each update and keep exact input/reply binding. a projection outage
should not erase the canonical task or justify a second executor.

## source boundaries

providers keep their repositories and releases. agent-connectors owns common
adapters and runtimes. operations conventions and domain work keep their own
sources. aiki owns common navigation, cross-component contracts and public
adoption material. it does not replace those runtimes or copy their identities.

## contracts versus implementations

the examples in this hub are proposed portable interchange contracts. they are
not the actual schemas of every provider. discover the real operation, inspect
its exact versioned schema and obey the current provider policy before use.
