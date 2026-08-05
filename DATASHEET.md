Datasheet for the BBO Capstone Project Data Set

Dataset name

BBO Capstone Project Sequential Query Data Set

Version

Version 1.0, documented on August 5, 2026.

Motivation

This data set was created to support a black-box optimisation (BBO) capstone project involving eight unknown objective functions. The goal of the project is to maximise the output of each function using a limited number of sequential queries. The dataset supports experimentation with Bayesian optimisation ideas, local search heuristics, surrogate-model thinking, and reflective analysis of how optimisation strategies evolve over time.

The dataset was not created to serve as a general-purpose machine learning benchmark. It was created specifically to document my own query history, observed outputs, and strategy changes throughout the capstone.

Composition

The data set contains input-output pairs for eight different black-box functions. Each input is a vector with values constrained to the range from 0 to 1, written to six decimal places. Each output is a single scalar response value returned by the course platform after a query was submitted.

The function dimensions are:

- Function 1: 2 inputs
- Function 2: 2 inputs
- Function 3: 3 inputs
- Function 4: 4 inputs
- Function 5: 4 inputs
- Function 6: 5 inputs
- Function 7: 6 inputs
- Function 8: 8 inputs

As of this datasheet version, the observed dataset contains:

- 8 functions
- 9 observed query rounds per function
- 72 total observed query-output pairs

The dataset is stored in text form as sequential lists of input arrays and output values. It includes the initial course-provided starting points and the subsequent manually submitted query points from later rounds.

Known gaps and limitations include:

- very sparse coverage of each search space
- increasingly uneven sampling because later rounds concentrate on promising regions
- no access to gradients, uncertainty labels, or true function definitions
- limited observations for the higher-dimensional functions
- no metadata about noise, smoothness, or local/global optimality

Collection process

The dataset was collected over multiple weekly capstone rounds. In each round, one new query point was proposed for each of the eight functions and submitted to the platform. The returned output was then appended to the growing history.

The query generation strategy changed over time:

- Round 1 focused on valid baseline submissions and initial coverage.
- Round 2 emphasised exploration by moving far from the first points.
- Rounds 3 to 5 used simple directional heuristics based on whether earlier outputs improved or worsened.
- Rounds 6 to 10 used more conservative local refinement, continuing stable improvement directions while pulling back when aggressive extrapolation appeared to hurt performance.

This means the data collection process is not random or uniformly designed. It is adaptive and path-dependent. Later samples are influenced by earlier observed outputs.

The main assumptions behind collection were:

- local output trends contain useful information for the next query
- nearby points can outperform earlier points if recent directionality is stable
- query efficiency matters more than broad global coverage once promising regions have been identified

Preprocessing and uses

The raw input values were not standardised or normalised beyond the original course constraint that every coordinate lies between 0 and 1. The main preprocessing applied was organisational rather than mathematical:

- grouping queries by round and by function
- formatting query strings to six decimal places
- manually reviewing output trends to guide later submissions

No label transformation, dimensionality reduction, or target scaling was required for the basic sequential optimisation workflow.

Intended uses

- documenting the sequential optimisation history of this capstone
- analysing how query strategies changed across rounds
- supporting simple surrogate-model experiments or local heuristic comparisons
- illustrating optimisation trade-offs such as exploration versus exploitation

Inappropriate uses

- training a general-purpose predictive model for unrelated tasks
- claiming strong statistical generalisation beyond this capstone
- fairness, safety, or policy analysis
- benchmarking large machine learning models without acknowledging the tiny sample size and path-dependent collection process

Distribution and maintenance

This dataset summary is intended to be documented in the public GitHub repository for the capstone project. The raw values originated from a course platform, so redistribution should respect the platform’s terms of use and any course policies about challenge data.

The repository owner maintains this dataset record by:

- appending new round queries and outputs
- updating this datasheet as the number of observed rounds increases
- documenting strategy changes and dataset limitations

Recommended maintenance actions include:

- storing the raw query and output history in a dedicated `data/` folder
- versioning observed data by round
- clearly separating observed data from proposed-but-not-yet-evaluated query points

Relationship to transparency

This datasheet improves transparency by making explicit:

- why the dataset exists
- how the samples were chosen
- what assumptions guided collection
- what kinds of conclusions should and should not be drawn from it

Because the dataset is small, adaptive, and intentionally non-random, these disclosures are important for anyone trying to interpret results or reproduce the capstone workflow.
