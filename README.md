# Data Privacy in Machine Learning

This repo contains code, simulation, and analysis from CS 591S1: Data Privacy in Machine Learning.

The code here is either from Homework, course project, or my own take or attempts at implementing some interesting and fun things inspired from the course.


## Homework 1
Contains two experiments:
* Attacks: two attacks using (a) The Hadamard attack (b) Random query attack.
  We have a mechanism that publishes results on the form
  ```
  a = 1/n Bx + y
  ```
  where B is either a n-by-n Hadamard matrix, or a random binary matrix of size m-by-n,
  where n is the number of elements in our dataset, and m is the number of queries.
  
  The hadamard attack is fast, and utilizes the fact that the Hadamard matrix H has a well known inverse.
  The random query attack is slower, as it needs m > n to get accurate results. It also runs least_squares optimization.
  
* Running Counter: Cute example where we want to release information about how often people click on certain ads per time interval.
