# adoption

begin with one useful outcome and your existing client. public source and an
installation recipe are prerequisites for a public installation claim. the public
telegram provider is the available starting implementation in this release.
other entries describe existing private implementations or portable patterns.

## first component

1. read the selected component's source recipe and license.
2. use your own account, sessions and isolated local state.
3. verify the intended identity and discover the required operation.
4. perform one useful authorized read or action and verify its result.
5. restart and continue without losing state or duplicating an effect.
6. try an isolated upgrade and verify the documented rollback.

for guarded messaging actions, preserve the provider's preview, confirmation,
account policy and independent readback. for a paid operation, identify the exact
authority and budget. installing a skill never supplies spending permission.

## first composition

connect two already accepted components. test the handoff, shared identity and
state owner. inject a disconnect after dispatch and show that recovery reconciles
the existing effect. keep actual installation requirements and receipts private
where they contain identities. publish a synthetic or sanitized receipt only.

## a useful receipt

record version/artifact, host/os, client, recipe, configuration boundary,
operation, independent result, restart/upgrade/rollback behavior and remaining
unknowns. see [synthetic acceptance](../examples/acceptance.json). an example
receipt does not count as acceptance of a real installation.
