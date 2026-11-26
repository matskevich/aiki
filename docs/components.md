# component map

the catalog separates reusable runtime, provider, policy, projection and domain
roles. a layer can have multiple implementations; the links name the current
source owners rather than a mandatory stack.

| component | role | depends on | optional composition |
| --- | --- | --- | --- |
| telegram | provider | none | conversation, tasks |
| whatsapp | provider | none | conversation, tasks |
| catalog | runtime | none | providers and devices |
| browser | runtime | none | device stages, tasks |
| android | runtime | none | tasks, payments |
| tasks | runtime | none | orchestration, conversation |
| orchestration | runtime | tasks | browser/android stages, watches |
| watches | runtime | tasks | orchestration, provider events |
| conversation | runtime | tasks | telegram or whatsapp, voice |
| context-skills | policy | none | every relevant task |
| operations | policy | context-skills | messaging, calendar, tasks |
| notifications | runtime | tasks | push providers and reply surfaces |
| linear | projection | tasks | operations and domain projects |
| payments | policy | context-skills | android/browser/provider, tasks |
| voice | runtime | none | conversation and speech providers |
| media | provider | none | browser/device stages, domain work |
| credentials | infrastructure | none | each installation's providers |
| content | domain | none | common tasks, media, operations |

required dependencies in this catalog describe the offered capability, not every
import dependency of the current package. shared packaging and independent
module packaging differ. the owning recipe remains authoritative for actual
installation requirements. [catalog data](../registry/components.json) records
this distinction and source visibility explicitly.
