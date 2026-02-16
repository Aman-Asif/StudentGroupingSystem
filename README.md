# Automated Student Grouping System

Python-based object-oriented system that forms optimized student groups using survey data and algorithmic grouping techniques.

## Features
- Models students, courses, surveys, and questions using OOP principles
- Supports multiple question types and evaluation criteria
- Weighted scoring system for group quality evaluation
- Multiple grouping algorithms:
  - Alphabetical Grouper
  - Greedy Grouper
  - Simulated Annealing Grouper
- Unit tested using pytest
- Static analysis compliant (PyTA / PEP8)

## Algorithms Implemented
- Deterministic alphabetical grouping
- Greedy optimization based on survey scores
- Simulated annealing for probabilistic global optimization

## Files
- `course.py` – Course and student management
- `survey.py` – Survey, scoring, and weighting logic
- `criterion.py` – Group evaluation criteria
- `grouper.py` – Grouping algorithms
- `tests.py` – Unit tests

## Example Output
Run `example_usage.py` to generate group visualizations.

## Tech Stack
Python, OOP, Algorithm Design, Unit Testing
