# Datasheet: BBO Capstone Observation History

## Motivation

This dataset documents a sequential black-box optimisation capstone. It supports the task of choosing input vectors for eight unknown functions when only a returned scalar score is observed. It was created to study low-budget optimisation, not to train a general-purpose predictive model.

## Composition

The versioned dataset is [`data/observations.csv`](data/observations.csv). It contains 88 query-output pairs: 11 recorded rounds for each of eight functions.

| Function | Input dimension | Observations |
| --- | ---: | ---: |
| Function 1 | 2 | 11 |
| Function 2 | 2 | 11 |
| Function 3 | 3 | 11 |
| Function 4 | 4 | 11 |
| Function 5 | 4 | 11 |
| Function 6 | 5 | 11 |
| Function 7 | 6 | 11 |
| Function 8 | 8 | 11 |

Each row contains a function identifier, round number, scalar output, and a pipe-separated input vector. Every input coordinate is bounded in `[0, 1]`. The original course-platform files are not redistributed beyond this documented history.

Known gaps include sparse high-dimensional coverage, no gradients, no true function formulas, no repeated evaluations for robust noise estimation, and no final response for the final recommended queries.

## Collection Process

One query per function was submitted in each recorded round. The platform returned an output after submission, and that feedback informed the next choice. Early queries explored more broadly; later choices increasingly refined strong regions. The data is therefore adaptive and path-dependent rather than an independent random sample.

## Preprocessing And Uses

The stored coordinates require no scale transformation because the portal constrains them to `[0, 1]`. The analysis rank-normalises outputs inside each function only for surrogate fitting. This preserves relative order while preventing the very different numeric ranges of the eight functions from dominating implementation choices.

Appropriate uses include capstone reporting, teaching acquisition functions, and reproducing the repository's retrospective analysis. Inappropriate uses include claiming a global optimum, making high-stakes decisions, or generalising performance beyond these eight hidden functions.

## Distribution And Maintenance

The processed observation history and analysis code are intended for the public capstone repository. The original source data belongs to the course context and remains subject to its terms. The repository owner maintains this datasheet, the CSV schema, and the alignment between data, code, generated reports, and documentation.
