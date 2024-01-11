# Suggesting an Actor for a Case

```mermaid
flowchart TB
    subgraph as:Offer
        RecommendActor
    end
    subgraph as:Accept
        AcceptActorRecommendation
    end
    subgraph as:Reject
        RejectActorRecommendation
    end
    subgraph as:Invite
        RmInviteToCase
    end
    RecommendActor --> a{Accept?}
    a -->|y| AcceptActorRecommendation
    a -->|n| RejectActorRecommendation
    AcceptActorRecommendation --> RmInviteToCase
```

## Recommend Actor

```python exec="true" idprefix=""
from vultron.scripts.vocab_examples import recommend_actor, json2md

print(json2md(recommend_actor()))
```

## Accept Actor Recommendation

```python exec="true" idprefix=""
from vultron.scripts.vocab_examples import accept_actor_recommendation, json2md

print(json2md(accept_actor_recommendation()))
```

## Reject Actor Recommendation

```python exec="true" idprefix=""
from vultron.scripts.vocab_examples import reject_actor_recommendation, json2md

print(json2md(reject_actor_recommendation()))
```

{% include-markdown "./_invite_to_case.md" heading-offset=1 %}




