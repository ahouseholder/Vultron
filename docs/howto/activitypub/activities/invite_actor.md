# Inviting an Actor to a Case

```mermaid
flowchart LR
    subgraph as:Invite
        RmInviteToCase
    end
    subgraph as:Accept
        RmAcceptInviteToCase
    end
    subgraph as:Reject
        RmRejectInviteToCase
    end
    subgraph as:Add
        AddParticipantToCase
    end
    RmInviteToCase --> a{Accept?}
    a -->|y| RmAcceptInviteToCase
    a -->|n| RmRejectInviteToCase
    RmAcceptInviteToCase --> AddParticipantToCase
```

{% include-markdown "./_invite_to_case.md" heading-offset=1 %}

## Accept Invite to Case

```python exec="true" idprefix=""
from vultron.scripts.vocab_examples import accept_invite_to_case, json2md

print(json2md(accept_invite_to_case()))
```

## Reject Invite to Case

```python exec="true" idprefix=""
from vultron.scripts.vocab_examples import reject_invite_to_case, json2md

print(json2md(reject_invite_to_case()))
```

## Add Participant to Case

```python exec="true" idprefix=""
from vultron.scripts.vocab_examples import add_coordinator_participant_to_case, json2md

print(json2md(add_coordinator_participant_to_case()))
```
