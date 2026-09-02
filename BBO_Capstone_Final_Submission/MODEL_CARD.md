# Model Card: Transparent GP Surrogate for BBO Retrospective Analysis

## Overview

**Version:** 2.0  
**Model type:** Gaussian-process surrogate with acquisition-based candidate selection  
**Implementation:** NumPy only; no external optimiser or cloud service

The model card describes the final reusable analysis implementation in `src/bbo_capstone/`. It is a retrospective model built from the documented capstone history. It should not be interpreted as a claim that the same implementation generated every historical portal submission.

## Intended Use

Suitable uses:

- teaching and demonstrating sequential black-box optimisation
- producing a reproducible next-query recommendation from small, bounded datasets
- comparing UCB, Expected Improvement, and posterior-variance acquisition behaviour
- discussing uncertainty, exploration, exploitation, and low-data limitations

Avoid using this model for high-stakes, safety-critical, or production decisions. It is not calibrated for real-world deployment, does not know the hidden objective function, and has not been validated beyond the capstone data.

## Inputs And Outputs

Input is a set of observed pairs `(x, y)` for one function, where `x` is a 2D to 8D vector constrained to `[0, 1]` and `y` is a scalar objective to maximise.

Output is one proposed next query, plus a predicted rank score, posterior uncertainty, and leave-one-out rank MAE. Predicted ranks are clipped to `[0, 1]` because the rank target is bounded. The proposed point is an experiment to evaluate, not a guaranteed optimum.

## Method

1. Rank-normalise observed output values within a function.
2. Fit a fixed-length-scale RBF Gaussian process with a small noise term.
3. Generate global candidates and local perturbations around the three best observations.
4. Score candidates with a selected acquisition function.
5. Return the top-scoring unseen candidate.

The fixed kernel is a deliberate regularisation choice. With 11 observations per function, optimising many kernel hyperparameters would make the surrogate appear more precise than the data warrants.

## Performance

The project treats every function as a maximisation problem. The primary observed metric is the best returned objective value per function. The model workflow also reports leave-one-out rank MAE, which measures how consistently the surrogate reproduces the relative ordering of observed points.

LOO rank MAE is a diagnostic, not a guarantee of generalisation. It is intentionally reported alongside uncertainty because a low error on a small, adaptively collected dataset can still be misleading.

## Assumptions And Limitations

- Similar input vectors are assumed to have broadly similar objective ranks.
- The observation history is sparse, adaptive, and increasingly concentrated around promising areas.
- Rank normalisation makes functions comparable for modelling but removes information about the size of output changes.
- A fixed isotropic kernel may miss interactions or different sensitivities across input dimensions.
- Candidate generation may under-sample an undiscovered region containing a better optimum.
- Posterior uncertainty is a model-based estimate, not direct knowledge of the true hidden function.

## Ethical And Transparency Considerations

The repository keeps the observed history in a readable CSV, documents the acquisition rules, fixes random seeds, and labels the final workflow as retrospective. These choices make it easier for a reviewer to reproduce the analysis, identify assumptions, and adapt the approach responsibly rather than treating model output as unquestionable evidence.
