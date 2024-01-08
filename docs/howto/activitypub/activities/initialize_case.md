# Initializing a Case

```mermaid
flowchart LR
    subgraph as:Create
        CreateCase
    end
    subgraph as:Add
        AddReportToCase
        AddParticipantToCase
        AddNoteToCase
    end
    CreateCase --> AddReportToCase
    CreateCase --> AddParticipantToCase
    CreateCase --> AddNoteToCase
```

{% include-markdown "./_create_case.md" heading-offset=1 %}
{% include-markdown "./_add_report_to_case.md" heading-offset=1 %}
{% include-markdown "./_add_participant_to_case.md" heading-offset=1 %}
{% include-markdown "./_add_note_to_case.md" heading-offset=1 %}
