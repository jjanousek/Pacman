# Pacman
Code I submitted as part of my course work in my Artificial Intelligence course at King's College.

My code can be found in the file partialAgents.py

## Report

https://github.com/jjanousek/Pacman_cw1/blob/master/cw1_Report.pdf

## Executive Summary

In this coursework, Pacman has only partial observability of his environment. I implemented the Breadth-First Search algorithm to find paths to the nearest food capsules and to evade ghosts.

## How to start a game using my PartialAgent
cd into your local Pacman folder and start with the terminal command below:

`python pacman.py --pacman PartialAgent --layout mediumClassic --numGames 50`

## Course work instructions
### 1. Introduction

This coursework exercise asks you to write code to control Pacman in the standard grid that we used for the practical exercises.

### 2. Getting started

You should download the file pacman-cw1.zip from KEATS. This contains a familiar set of files that implement Pacman, and version 3.0 of api.py which defines the observability of the environment that you will have to deal with.
Version 3 of api.py (which you will already have met if you worked through Practical 3), further restricts Pacman’s view of the world beyond what it was. Now, if they are moving, Pacman can only see food and capsules ahead along the corridor (that is in the same direction as Pacman is heading) up to the same 5 step distance that was possible before with Version 2. However, in this case, if there is a wall less than 5 steps away, visibility stops at the wall. If Pacman is passing a side corridor, they can see one step down that corridor (out of the corner of their eye).
With the new api.py, ghosts can be seen just like food and capsules — ahead if Pacman is moving, and forwards and backwards (and left and right if there are corridors) when Pacman is stationary.
Since Pacman moves at the same speed as the ghosts, not being able to see ghosts behind should not be a problem — if Pacman is moving, it can’t be caught by a ghost behind, and if it reverses direction, the 5 steps are a cushion that should allow Pacman to stop before a ghost that is behind catches them. However, as a bonus, Pacman can always detect a ghost that is 2 steps or less away. (Perhaps Pacman can hear the ghosts move.) This means that Pacman should be able to avoid colliding with a ghost in the intersection of two corridors, something that can’t be avoided if Pacman can only see along corridors.

### 3. What you need to do

### 3.1 Write code

This coursework requires you to write code to control Pacman and win games despite the limitations that api.py places on observability. There is a (rather familiar) skeleton piece of code to take as your starting point in the file partialAgents.py. This code defines the class PartialAgent.
There are two main aims for your code:
(a) Be able to win games when there are no ghosts.
(b) Be able to win one game in five, on average, when there are ghosts.
To win games, Pacman has to be able to eat all the food. For this coursework, “winning” just means getting the environment to report a win. Score is irrelevant.

### 3.2 Things to bear in mind

Some things that you may find helpful:
(a) We will evaluate whether your code can win a game when there are no ghosts by running:
`python pacman.py -p PartialAgent -l mediumClassicNoGhosts` -l is shorthand for -layout. -p is shorthand for -pacman.
(b) We will evaluate whether your code can win a game when there are ghosts by running:
`python pacman.py -n 5 -p PartialAgent -l mediumClassic` The -n 5 runs five games in a row.
(c) When using the -n option to run multiple games, the same agent (the same instance of partialAgent.py) is run in all the games.
That means you might need to change the values of some of the state variables that control Pacman’s behaviour in between games. You can do that using the final() function.
(d) You are not required to use any of the methods described in the practicals.
(e) If you wish to use any of the code I provided (such as that for CornerSeekingAgent and so on), you may do this, but you need to include comments that explain what you used and where it came from (just as you would for any code that you make use of but don’t write yourself ).
(f) You can only use libraries that are part of a the standard Python 2.7 distribution. This ensures that (a) everyone has access to the same libraries (since only the standard distribution is available on the lab machines) and (b) we don’t have trouble running your code due to some library incompatibilities.

### 3.3 Write a report

Write up a description of your program along with your evaluation in a separate report that you will submit along with your code.
As you work through your implementation of Pacman’s strategy, you will find that you are making lots of decisions about how precisely to translate your ideas into working code. The report should explain these at length. The perfect report will give enough detail that we don’t feel we have to read your code in order to understand what you code does (we will read it anyway).
Remember, when doing this, that there is credit for creative and beautiful solutions. Make sure you highlight these aspects of your work, especially things that make your work unique.
Having said that, reports that are needlessly long will not get any more credit. We value concise reports (we have to read a lot of them). Your report should also analyse the performance of your code. Because there is a certain amount of randomness in the behaviour of the ghosts, a good analysis will run multiple games to assess Pacman’s performance. For example, you might like to try running:
`python pacman.py -n 50 -p PartialAgent -l mediumClassic`
to get a statistically significant number of runs. (Of course, to decide whether this was a statistically significant number of runs, you would have to do some statistical analysis — it might well need more runs.) All the conclusions that you present in your analysis should be justified by the data that you have collected.

