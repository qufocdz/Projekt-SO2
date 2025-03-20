# Project-SO2
## Part 1 - N-Philosophers Problem
### Description
  The first assignement of the project is realised in the philo_problem directory. The goal was to present a solution to the classical N-Philosophers Problem.
  N-Philosophers share N-chopsticks (if there is only one Philosopher then he gets to keep 2 chopsticks for himself). The chopsticks are placed inbetween the philosophers.
  When a Philosopher wants to eat, he tries to pick up the chopsticks next to him. This problem revolves around finding a way to organize philosophers behavior in a way that prevents them from blocking everyone from eating (deadlock).
  Such a situation may occur when every single one of philosophers reaches for their left chopstick at the same time. Once they take hold of a chopstick, they cannot release it without having eaten first - which means they are stuck in this state.
  
### Installation and usage
1. Clone the repository.
2. Either compile the main.cpp file (C++11 at least for to_string() to work) or find philo_problem.exe in philo_problem/x64/Debug directory.
3. Run philo_problem.exe.
4. Enter the number of philosophers and watch the program run.
   
