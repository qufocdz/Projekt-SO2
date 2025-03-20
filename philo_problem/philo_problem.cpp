#include <iostream>
#include <string>
#include <thread>
using namespace std;

//making a global pointer for chopstick array
int* chopstick;

void wait(int& semaphore)
{
    //active waiting
    while (semaphore <= 0)
    {
        ;
    }
    semaphore--;
}

void signal(int& semaphore)
{
    //signaling the semaphore is free
    semaphore++;
}

void philo_process(int id, int max_philo)
{
    string eating = "Philosopher nr. " + to_string(id + 1) + " starts eating.\n";
    string thinking = "Philosopher nr. " + to_string(id + 1) + " starts thinking.\n";

    if (max_philo == 1)
    {
        max_philo = 2; //making sure solo philosopher can eat
    }

    do {
        if (id % 2 == 0) //creating asymmetry so that all the philosophers won't reach for the same side chopstick first - preventing deadlock
        {
            //philosopher waits for both chopsticks he needs
            wait(chopstick[id]);
            wait(chopstick[(id + 1) % max_philo]);
            cout << eating;
            this_thread::sleep_for(chrono::milliseconds(rand() % 2001 + 1000)); //philosopher takes his time eating - his critical section

            //philosopher signals he is done eating and the chopsticks are free
            cout << thinking;
            signal(chopstick[id]);
            signal(chopstick[(id + 1) % max_philo]);
            this_thread::sleep_for(chrono::milliseconds(rand() % 2001 + 1000)); //philosopher takes his time thinking
        }
        else
        {
            //philosopher waits for both chopsticks he needs
            wait(chopstick[(id + 1) % max_philo]);
            wait(chopstick[id]);
            cout << eating;
            this_thread::sleep_for(chrono::milliseconds(rand() % 2001 + 1000)); //philosopher takes his time eating - his critical section

            //philosopher signals he is done eating and the chopsticks are free
            cout << thinking;
            signal(chopstick[(id + 1) % max_philo]);
            signal(chopstick[id]);
            this_thread::sleep_for(chrono::milliseconds(rand() % 2001 + 1000)); //philosopher takes his time thinking
        }

    } while (true); //because the only thing the philosopher can do is either think or eat forever
}

int main()
{
    //initializing random number generator
    srand((time(0)));

    int philo_num;
    int chop_num;
    cout << "Enter the number of philosophers: ";
    cin >> philo_num;

    //making sure solo philosopher can eat
    if (philo_num == 1)
    {
        chop_num = 2;
    }
    else
    {
        chop_num = philo_num;
    }

    //creating chopstick semaphores dynamically
    chopstick = new int[chop_num];
    for (int i = 0; i < chop_num; i++)
    {
        chopstick[i] = 1; //all chopsticks are available at first
    }


    //creating philosopher threads dynamically
    thread* philosophers = new thread[philo_num];
    for (int i = 0; i < philo_num; i++)
    {
        philosophers[i] = thread(philo_process, i, philo_num);
    }

    while (true) {} //so the program doesn't end
    return 0;
}