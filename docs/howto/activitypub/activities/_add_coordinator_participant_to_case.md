# Add Participant to Case

The vendor adds a coordinator participant to the case.

```python exec="true" idprefix=""
from vultron.scripts.vocab_examples import add_coordinator_participant_to_case, json2md

print(json2md(add_coordinator_participant_to_case()))
```

!!! tip "Avoid bogging down in details"

    Adding a participant to a case involves creating the participant object and a participant status object.
    As we discuss elsewhere, it's probably overkill to emit separate `as:Create` and `as:Add` events for each
    of these events.

    ```mermaid
    flowchart LR
    
    a[create participant] --> b[create participant status]
    b --> c[add participant status to participant]
    c --> d[add participant to case]
    ```
   
    Instead, we could emit a single `as:Create` event for the participant, already containing a status object, and
    have the `target` of the `as:Create` event be the case object.

    ```mermaid
    flowchart LR
    a[create particpant with status] -->|target| b[case]
    ```

