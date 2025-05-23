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
### Description
The second assignement of the project is realised in the chat_server directory. The goal was to create a multithreaded chat server capable of creating a new thread for each client connection and synchronizing the communication between clients.
This problem vaguely resembles the classical Readers-Writers problem, in which many readers can access one resource, but when a resource is being modified by a Writer, only he can have access to it.
The twist is, Client can remain silent, be a Reader and only read the data sent to him, or he can become a Writer at any time and send his own message, acquiring resources needed to broadcast his message to everyone.
The synchronization issue appears when a few Clients want to become a Writer at the same time, which is a race condition, and also when one of Clients disconnects/connets when being broadcasted to, which modifies the connections list the Writer operates on.

### Installation and usage
1. Clone the repository.
2. Run the server by either:
   2.1. Using python ./server.py.
   2.2. Finding ./dist/server.exe and executing it.
3. Run up to 5 clients by:
   3.1. Using python ./client.py.
   3.2. Finding ./dist/client.exe and executing it.
5. For each open client, set a nickname to enter chat.
6. Each client now has access to chat server and can type and send their messages.

### Solution
In order to solve the multithreaded chat server's Writers-Readerslike problem I implemented a solution consisting of Mutex Locks.
I used Mutex Locks from Python's Threading library:
- broadcast_mutex - blocks the access to shared ability of broadcasting a message, which makes sure the message history is in order,
- connection_mutex - blocks the access to connections_list, which is made up of ClientConnection threads, as it can be modified by various threads during it's lifetime,
  
Then I also created a ClientConnection class extending Thread, overwritting the Thread's run method with one that receives messages and tries to broadcast them in a manner discussed below.
I also added methods to handle the disconnection and a few parameters with Client's info.

**Explanation of solution:**
- Client Connections = extended Threads.
- Server has one shared resource, which is connections list and one shared ability, which is broadcasting (meaning at any time only one Client Connection thread can broadcast).
- Provided a Connection Mutex Lock and a Broadcast Mutex Lock.
- The servers main program listens for TCP connections in which a Client introduces themselves via nickname.
- When this occurs, server tries to acquire Connection Mutex Lock in order to add the Client to connections list. This ensures the list isn't being used by a Writer at this moment.
- Server adds the Client Connection thread and starts it. Each Client Connection's thread activity is trying to receive data from Client and then broadcast it.
- In order for the Client Connection to broadcast, it must first acquire Broadcast Mutex Lock and a Connection Mutex Lock, afterwards the thread reaches it's full critical section.
- The Client Connection list is copied and Connection Mutex Lock is released in order to free up the resource earlier - it won't matter if a new Client joins now or someone leaves, because it is already set who was a part of communication at that time.
- The Client Connection can now safely broadcast it's message to everyone. Afterwards it releases its Broadcast Mutex Lock, fully exiting the critical section.
- It is also worth to mention, when a Client Connection is being terminated, it also acquires the Connection Mutex Lock in order to not modify the connection list when it is being used by another thread.
- Furthermore, the Client side application also contains two threads, one of them is used for receiving a messange and the other one is used for sending a message - this process however does not use any shared resources on the Client side.
  
