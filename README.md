# PythonGeneticAlgorithmMaze
 A visualized maze solver using genetic algorithms of various complexity, uses game engine logic to give each agent velocities. This project aims to give an intuitive rundown of what genetic algorithms are, what they can achieve, what their setbacks are, and how they slowly build to the more advanced methods of artificial intelligence that we see today.

Naive Genetic Algorithm Approach:

You can run this version by selecting the "naive direction genetic agent" option

The first genetic agent defined uses the most basic genetic algorithm approach:

Their genetic sequence is comprised of a list of 2d vector directions, with the agent constantly moving forward and turning between them at a given rate.

This is equivalent of blindfolding a bunch of drivers, putting a brick on the gas pedal, and telling them to turn.

Eventually through the process of evolving, the sequence of directions ends up forming a path closer and closer to reaching the goal without colliding. Albeit with still a significant amount of random collisions within each generation.

There are a few issues with this naive approach:

Is not applicable to different mazes/obstacle courses. Since the genetic sequence is just a simple list of directions, the evolution targets itself to just evolve to that specific obstacle course.

Local maxima become a big issue: Just as in gradient descent, there is a significant problem with fitting towards local fitness maxima. Currently the fitness function, that determines evolution, is merely a measure of how far away the final position of an agent is from the goal. This can easily cause the issue of a local fitness maxima if the agents can get close to the goal while hitting a dead end, with the correct path requiring the agents to move further away from the goal before being able to successfully reach it. If only the highest "fitness" agents influence successive generations, they will all evolve into hitting the local maxima as any agent that attempts to veer off the path will get punished for a worse fitness value. 

While it is possible to adjust the parameters of the algorithm, by increasing the amount of surviving stragglers, increasing the mutation rate, and loosening the cutoff threshold, this again can cause issues with even more extreme complex mazes and require a rapidly increasing amount of generations to solve. 

