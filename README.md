README: BBO Capstone Project

This repository contains the materials, notes, and working files for my Black-Box Optimisation (BBO) Capstone Project. For each function, I describe the objective of the challenge, the data constraints, and the decision-making process I used to test different machine learning ideas.

Why Black-Box Optimisation

Black-Box Optimisation is important because many real-world systems do not reveal how they work internally. In these cases, we only observe the inputs we try and the outputs we receive. The internal function is hidden, so the task is to learn from outcomes and make better decisions over time.

This is relevant in machine learning, engineering, science, and business, where we often need to improve performance without having access to gradients, equations, or fully interpretable models.

For me, this project is also a way to build practical understanding of what an ML model can learn from limited data, how decisions can be made under uncertainty, how optimisation strategies improve with more observations, and how model behaviour can be tested and explained in a black-box setting.

Project Overview

This project is based on a Bayesian or Black-Box Optimisation competition involving 8 unknown functions.

Each function is treated as a maximisation problem, where the objective is to find the set of input values that gives the highest possible output.

Because the true function is unknown, the project is not only about finding good values, but also about learning how to explore the search space efficiently, exploit promising regions, compare modelling strategies, and refine queries across multiple rounds.

Repository Contents

This project is structured around the following types of files:

initial_data
extended_data
Jupyter notebooks
README.md
DATASHEET.md
MODEL_CARD.md

Initial Data

The initial dataset contains the starting samples for the 8 functions. Each function has input values and output values. These starting observations are used for first-stage exploration and analysis.

Extended Data

Each week, one new query is submitted for each function. This creates a growing dataset over time.

The extended data records new submitted query points, returned output values, and changes in strategy from week to week.

Helper Notebooks

The notebooks are used to support different parts of the project, such as exploratory data analysis, regression-based inspection, feature comparisons, manual query tracking, and testing different ML methods.

Inputs and Outputs

The model receives a query point for one of the unknown functions.

Each query is written as:

x1-x2-x3-...-xn

Each value is between 0 and 1, each value is written to six decimal places, and the number of values depends on the function dimension.

Example formats:

2D: 0.248731-0.672945
4D: 0.124578-0.739201-0.456890-0.281345

Each submitted query returns a single numerical response value. This output acts as the performance signal used to decide future queries.

Challenge Objectives

The main objective of this BBO project is to maximise the output value of each unknown function.

To do this, I need to work within several constraints. The function structure is unknown, only a limited number of queries can be made, no gradient information is available, and feedback is received only after submission.

Because of this, the project requires a balance between exploration, which means testing new or uncertain regions, and exploitation, which means focusing on regions that already look promising.

Technical Approach

This section is a living record of how my strategy changes across rounds.

Round 1

In the first round, I focused on making valid submissions and establishing an initial baseline. At this stage, the main goal was to start collecting information.

Round 2

In the second round, I leaned more toward exploration. I selected points that were far from my first queries so I could sample new regions of the search space.

Round 3

In the third round, I became more data-driven. After comparing the first two observed outputs for each function, I moved slightly beyond the better-performing point to follow the stronger local direction.

ML Methods Considered

Since this project involves continuous outputs and unknown nonlinear functions, I considered several approaches. These include Bayesian Optimisation concepts such as UCB, EI, and PI, regression ideas for identifying rough trends, SVM-based thinking for separating potentially high-performing and low-performing regions, and heuristic search when sample sizes are too small for reliable modelling.

At this stage, I do not rely on one fixed model. Instead, I adapt the method depending on the amount of data available and the behaviour of each function.

Current Understanding

One of the most important lessons from this project is that optimisation in black-box settings is iterative. Early rounds require broader exploration, while later rounds can become more targeted as more feedback is collected.

This project has helped me improve my understanding of optimisation under uncertainty, model limitations in small datasets, high-dimensional search problems, and practical reasoning in applied machine learning.

Work in Progress

This repository is a work-in-progress record of my capstone journey. As more weekly data becomes available, I will continue updating the query strategies, modelling notes, function-specific observations, and reflections on what worked and what did not.

Additional Documentation

To improve transparency and reproducibility, this repository also includes:

[Datasheet for the BBO dataset](DATASHEET.md)
[Model card for the optimisation approach](MODEL_CARD.md)
