Model Card for the BBO Optimisation Approach

Model name

Sequential Local-Trend Heuristic for Black-Box Optimisation

Version

Version 1.0, documented on August 5, 2026.

Overview

This model card describes the optimisation approach used in my BBO capstone project. The approach is not a single trained model in the usual machine learning sense. Instead, it is a sequential decision policy that uses observed query-output history to choose the next query point for each of eight unknown functions.

The method began with broad exploration and gradually shifted toward local refinement. It is best described as a lightweight optimisation framework informed by Bayesian optimisation ideas, but implemented mainly through transparent heuristics because the available dataset is very small.

Intended use

Suitable uses

- sequential black-box maximisation with very limited evaluation budgets
- educational optimisation tasks where transparency matters
- low-data settings where a simple heuristic is easier to justify than a complex surrogate model
- documenting the evolution of optimisation decisions across rounds

Uses to avoid

- high-stakes optimisation where rigorous uncertainty estimation is required
- large-scale automated optimisation without stronger validation
- claims of global optimality
- settings where smooth local trend assumptions are known to fail badly

Details of the approach

Round 1

I submitted valid baseline queries to establish a starting point for each function.

Round 2

I focused on exploration by moving far from the initial points to sample new regions.

Rounds 3 to 5

I compared the early observed outputs and used directional heuristics. If a move improved the function, I continued cautiously in a similar direction. If it hurt performance, I reduced the step or returned closer to the best earlier point.

Rounds 6 to 8

I became more conservative and function-specific. Functions with steady improvements were exploited more aggressively, while unstable functions were handled with smaller local refinements or pullback moves.

Rounds 9 and 10

I continued to use recent local trends as the main signal. At this stage, the strategy relied on distinguishing among three cases:

- continue in a stable improving direction
- refine locally if the gains are small but consistent
- reverse or retreat toward a prior stronger region if extrapolation weakens the output

The main techniques used across the ten rounds were:

- exploration in early rounds
- exploitation in later rounds
- local trend continuation
- step-size control
- fallback to best-known regions when performance deteriorated
- qualitative surrogate-model thinking without fitting a heavy model

Performance

The primary metric is the best observed output achieved so far for each function. Because the challenge is a maximisation task, larger outputs are better.

Best observed outputs in the currently documented history are:

- Function 1: 8.097753861412983e-75
- Function 2: 0.26844212669171835
- Function 3: -0.02750330035001966
- Function 4: -12.115525507270515
- Function 5: 570.163308771557
- Function 6: -1.0254478902479245
- Function 7: 0.5837394677006731
- Function 8: 8.625049475

Performance should be interpreted carefully because:

- the search spaces have different dimensionalities
- the scales of the function outputs differ substantially
- the optimisation history is adaptive rather than controlled
- later rounds were influenced by earlier observed outcomes

The model has worked best on functions where repeated local adjustments produced steady gains, especially Functions 5, 7, and 8. It has been weaker on functions that appear flat, noisy, or irregular, such as Functions 1, 4, and 6.

Assumptions and limitations

Key assumptions

- recent local behaviour contains useful information for choosing the next point
- nearby points can outperform previous ones if the direction of improvement is stable
- simple, interpretable heuristics are preferable to overfit surrogate models in a tiny-data setting

Main limitations

- sparse data, especially in higher dimensions
- heavy dependence on local trend assumptions
- possible sampling bias because later points cluster near previously promising regions
- no formal uncertainty quantification
- limited ability to detect better regions far away from the sampled path

Failure modes

- getting trapped near a local optimum
- overreacting to one unusually good or bad round
- missing strong regions in sparsely explored parts of the search space
- underperforming when the function is highly irregular or nonlocal

Ethical considerations

Transparency improves reproducibility in this project because the optimisation logic is explicit and can be audited. Rather than presenting the approach as a mysterious “smart search,” I document the rules, assumptions, and trade-offs behind each round of decision-making.

In real-world adaptation, this matters because practitioners often need to justify not only what decision was made, but why it was made and what evidence supported it. A transparent model card helps others evaluate whether the approach is suitable for their context and where it might fail.

Why this structure is useful

This model card is intentionally compact but sufficient for the current capstone stage. It explains:

- what the optimisation approach is
- what it is intended to do
- how it evolved across the ten rounds
- what performance signal is being used
- what assumptions and limitations matter most

Additional detail could be added later, such as per-round query tables or visualisations of search trajectories, but the current structure is enough to communicate the essential reasoning to peers, facilitators, and future employers.
