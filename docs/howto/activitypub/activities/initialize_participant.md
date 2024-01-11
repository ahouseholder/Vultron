# Initializing a CaseParticipant

```mermaid
flowchart LR
    subgraph as:Create
        CreateParticipant
    end
    subgraph as:Add
        AddParticipantToCase
    end
    RmCreateParticipant --> AddParticipantToCase
```

{% include-markdown "./_create_participant.md" heading-offset=1 %}
{% include-markdown "./_add_participant_to_case.md" heading-offset=1 %}
