# release boundaries

new original content in this repository is mit licensed. linked implementations
retain their own licenses and access controls. this license does not relicense
their code, data or private history.

## public artifact

use a clean tree and deliberate file list. inspect current files and reachable
history for credentials and personal data. exclude sessions, resolved secrets,
real task records, health information, private correspondence, account/device
identifiers and deployment receipts. signature scanning supplements a human
source review; it cannot prove absence of personal information.

## component release

keep source ownership and compatibility explicit. publish source checks,
packaging, intended-consumer acceptance and rollback separately. examples or
owner deployment experience do not establish independent recipient acceptance.

## lifecycle

prepare on a feature branch → validate metadata and links → review the diff and
artifact → merge → verify the published sha. each provider owns its own release
gate. a new capability or parameter needs an explicit mapping or documented gap
for downstream consumers. do not silently widen access or move a live account.
