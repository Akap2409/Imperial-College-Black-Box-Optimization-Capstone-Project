# Retrospective Optimisation Report

This report replays the recorded capstone observations using one transparent Gaussian-process surrogate and a UCB acquisition function. It is a retrospective analysis, not a claim that these exact proposals were used in every historical submission.

| Function | Dim | Best observed output | Proposed next query | Predicted rank | Uncertainty | LOO rank MAE |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| Function 1 | 2 | 1.3803111e-35 | `0.996053-0.473478` | 1.000 | 0.631 | 0.333 |
| Function 2 | 2 | 0.26844213 | `0.724435-0.000001` | 0.960 | 0.526 | 0.255 |
| Function 3 | 3 | -0.0275033 | `0.057012-0.999999-0.440167` | 0.769 | 0.711 | 0.279 |
| Function 4 | 4 | -12.115526 | `0.408170-0.554960-0.427832-0.414227` | 1.000 | 0.934 | 0.156 |
| Function 5 | 4 | 637.69267 | `0.000001-0.925827-0.162098-0.996203` | 1.000 | 0.785 | 0.114 |
| Function 6 | 5 | -0.99580435 | `0.248522-0.768802-0.536799-0.609616-0.331802` | 0.702 | 0.700 | 0.191 |
| Function 7 | 6 | 0.6052265 | `0.527086-0.234951-0.694294-0.173896-0.501745-0.539943` | 1.000 | 0.885 | 0.106 |
| Function 8 | 8 | 8.6433708 | `0.333481-0.667723-0.524259-0.537808-0.330313-0.889499-0.468148-0.103289` | 0.999 | 0.898 | 0.143 |

## Reading the metrics

- Lower leave-one-out rank MAE indicates that the small-data surrogate reproduces the relative ordering of observed outcomes more consistently.
- The predicted rank is clipped to the observed [0, 1] ranking scale; it and the uncertainty are not predictions of the original objective value.
- A candidate proposal is evidence for a next experiment, not evidence that the global optimum has been found.
