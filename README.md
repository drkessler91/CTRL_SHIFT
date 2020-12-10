# CTRL_SHIFT
Final Project, B.Sc. in Computer Science

An AI system, for scheduling ground attendants shifts for 'EL-AL' flight company.
The algorithm we based our system on was Constraints Satisfaction Problem (CSP) and modified it to our problem. We chose the most constrained variable heuristic as our main goal - which flight has the most overlap time with other flights and it will be assigned with attendants first in order.
The system can handle around 150 attendants and 600 flights per week. 

The development  was in Python, while we used Django framework for creating the web interface for the shift display.
MySQL database.

The System enabled reduce of the time needed for the shift manager to make complete shift board, from 1 hour and half to several seconds and, by making a web interface, no waste of papers happened  - Hello (Green) World!
