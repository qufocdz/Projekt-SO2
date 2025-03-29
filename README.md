# Project-SO2
## Part 1 - N-Philosophers Problem
### Description
  The first assignement of the project is realised in the philo_problem directory. The goal was to present a solution to the classical N-Philosophers Problem.
  N-Philosophers share N-chopsticks (if there is only one Philosopher then he gets to keep 2 chopsticks for himself). The chopsticks are placed inbetween the philosophers.
  When a Philosopher wants to eat, he tries to pick up the chopsticks next to him. This problem revolves around finding a way to organize philosophers behavior in a way that prevents them from blocking everyone from eating (deadlock).
  Such a situation may occur when every single one of philosophers reaches for their left chopstick at the same time. Once they take hold of a chopstick, they cannot release it without having eaten first - which means they are stuck in stalemate state.
  
### Installation and usage
1. Clone the repository.
2. Use makefile to compile code or find philo_problem.exe in ./x64/Debug directory.
3. Run philo_problem.exe.
4. Enter the number of philosophers and watch the program run.

### Solution
In order to solve the N-Philosophers problem I implemented a solution consisting of mutex semaphores and asymmetric chopstick picking up order.
I implemented the following functions for semaphores:
- wait(int& semaphore) - It's a basic semaphore function called by a thread that wants to get access to a resource. It has to actively wait for the semaphores value to be at least 1.
- signal(int& semaphore) - It's a basic semaphore function called by a thread that wants to signal he doesn't use the resources anymore and they are free to pick up.
  
Then I also implemented the following function for threads:
- philo_process(int id, int max_philo) -  It's a function that defines the behaviour of all the Philosophers. They prepare their messages, and then an infinite loop of eating and thinking starts.

The process of creating chopstick semaphores and and Philosopher threads is handled dynamically in main(). The program runs indefinitely, the same way Philosophers eat and think indefinitely.

**Explanation of solution:**
- Philosopher = Threads, Chopsticks = Semaphores.
- Each philosopher first waits for both the chopsticks he needs (determined by modulo operation on indexes). The chopsticks are semaphores that the Philosopher thread uses wait() function on.
- After acquiring both the chopsticks, Philosopher enters his **Critical State** - he starts eating.
- Philosopher decides to stop eating - he releases his chopsticks by calling signal() function on them. Philosopher exits his **Critical State** - he starts thinking.
- **Unfortunately it's not enough to prevent deadlock and starvation.** Therefore further measures are taken.
- Asymmetry heuristic is added in order to prevent deadlock. Even Philosophers first pick up their left chopstick and uneven Philosophers first pickup their right chopstick. This prevents a situation in which all Philosophers get hungry at the same time and pickup the chopsticks from the same side at the same time.
- Starvation prevention is implemented by randomizing the time it takes for philosophers to eat and think, which is a realistic assumption. This leads to every philosopher eventually having a window in which they can pickup both chopsticks.

## Part 2 - Multithreaded Chat Server
TBD
