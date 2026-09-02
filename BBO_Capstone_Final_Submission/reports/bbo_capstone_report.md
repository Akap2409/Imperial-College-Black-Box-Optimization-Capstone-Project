# BBO Capstone Report

This report summarises the optimisation history stored in `bbo_capstone_analysis.py`.
It focuses on the same strategy used across the capstone: broad exploration early, then conservative local refinement near the strongest observed regions.

## Summary Table

| Function | Dim | Observed rounds | Best output | Best query | Final submitted query |
| --- | ---: | ---: | ---: | --- | --- |
| Function 1 | 2 | 11 | 1.3803111223e-35 | `0.809000-0.497000` | `0.812000-0.505000` |
| Function 2 | 2 | 11 | 0.268442126692 | `0.583214-0.194876` | `0.582500-0.196500` |
| Function 3 | 3 | 11 | -0.02750330035 | `0.314000-0.851000-0.463500` | `0.313500-0.852500-0.463200` |
| Function 4 | 4 | 11 | -12.1155255073 | `0.124578-0.739201-0.456890-0.281345` | `0.124300-0.739300-0.456800-0.281300` |
| Function 5 | 4 | 11 | 637.69267301 | `0.000001-0.999999-0.305315-0.804063` | `0.000001-0.999999-0.294000-0.818000` |
| Function 6 | 5 | 11 | -0.99580434627 | `0.291000-0.706000-0.401000-0.579000-0.249000` | `0.297000-0.700000-0.404000-0.576500-0.257000` |
| Function 7 | 6 | 11 | 0.605226501863 | `0.671397-0.275247-0.881280-0.160741-0.475545-0.710927` | `0.674500-0.271500-0.885500-0.157500-0.475300-0.713500` |
| Function 8 | 8 | 11 | 8.643370775 | `0.140000-0.818000-0.403000-0.600000-0.293500-0.941000-0.466500-0.196000` | `0.145000-0.813000-0.404000-0.599000-0.295500-0.938000-0.466800-0.199000` |

## Function Notes

### Function 1
- Dimension: 2
- Best observed output: `1.3803111223e-35` at `0.809000-0.497000`
- Latest observed output: `3.85625486871e-88` at `0.775000-0.305000`
- Distance between latest and best observed point: `0.194987`
- Heuristic local-refinement proposal: `0.798406-0.458488`
- Final documented submission: `0.812000-0.505000`

### Function 2
- Dimension: 2
- Best observed output: `0.268442126692` at `0.583214-0.194876`
- Latest observed output: `-0.0147309405611` at `0.585500-0.192000`
- Distance between latest and best observed point: `0.003674`
- Heuristic local-refinement proposal: `0.586562-0.182932`
- Final documented submission: `0.582500-0.196500`

### Function 3
- Dimension: 3
- Best observed output: `-0.02750330035` at `0.314000-0.851000-0.463500`
- Latest observed output: `-0.0428765154431` at `0.316000-0.848000-0.463400`
- Distance between latest and best observed point: `0.003607`
- Heuristic local-refinement proposal: `0.308804-0.860975-0.462245`
- Final documented submission: `0.313500-0.852500-0.463200`

### Function 4
- Dimension: 4
- Best observed output: `-12.1155255073` at `0.124578-0.739201-0.456890-0.281345`
- Latest observed output: `-12.1405216556` at `0.124000-0.739500-0.456700-0.281200`
- Distance between latest and best observed point: `0.000693`
- Heuristic local-refinement proposal: `0.124539-0.739231-0.456812-0.281342`
- Final documented submission: `0.124300-0.739300-0.456800-0.281300`

### Function 5
- Dimension: 4
- Best observed output: `637.69267301` at `0.000001-0.999999-0.305315-0.804063`
- Latest observed output: `585.640577643` at `0.318500-0.783200-0.999999-0.000001`
- Distance between latest and best observed point: `1.130285`
- Heuristic local-refinement proposal: `0.042468-0.971092-0.398229-0.696386`
- Final documented submission: `0.000001-0.999999-0.294000-0.818000`

### Function 6
- Dimension: 5
- Best observed output: `-0.99580434627` at `0.291000-0.706000-0.401000-0.579000-0.249000`
- Latest observed output: `-0.99580434627` at `0.291000-0.706000-0.401000-0.579000-0.249000`
- Distance between latest and best observed point: `0.000000`
- Heuristic local-refinement proposal: `0.287479-0.709499-0.399244-0.580399-0.244777`
- Final documented submission: `0.297000-0.700000-0.404000-0.576500-0.257000`

### Function 7
- Dimension: 6
- Best observed output: `0.605226501863` at `0.671397-0.275247-0.881280-0.160741-0.475545-0.710927`
- Latest observed output: `0.575135727409` at `0.680500-0.265000-0.892500-0.151500-0.474800-0.718500`
- Distance between latest and best observed point: `0.021379`
- Heuristic local-refinement proposal: `0.672510-0.274011-0.882535-0.159704-0.475460-0.711816`
- Final documented submission: `0.674500-0.271500-0.885500-0.157500-0.475300-0.713500`

### Function 8
- Dimension: 8
- Best observed output: `8.643370775` at `0.140000-0.818000-0.403000-0.600000-0.293500-0.941000-0.466500-0.196000`
- Latest observed output: `8.62085357` at `0.128000-0.830000-0.399500-0.603500-0.287000-0.949500-0.465300-0.185000`
- Distance between latest and best observed point: `0.023440`
- Heuristic local-refinement proposal: `0.138317-0.819683-0.402508-0.600492-0.292617-0.942192-0.466332-0.194458`
- Final documented submission: `0.145000-0.813000-0.404000-0.599000-0.295500-0.938000-0.466800-0.199000`

## Interpretation

- Functions 2, 3, 4, 7, and 8 were handled mostly with exploitation because their stronger regions became stable over time.
- Functions 5 and 6 still showed directional movement later in the project, so their final queries kept a small exploration component.
- Function 1 remained difficult and low-signal, so the final choice stayed conservative rather than making a large jump.
