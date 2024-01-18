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
{% include-markdown "./_accept_invite_to_case.md" heading-offset=1 %}
{% include-markdown "./_reject_invite_to_case.md" heading-offset=1 %}
{% include-markdown "./_add_coordinator_participant_to_case.md" heading-offset=1 %}
