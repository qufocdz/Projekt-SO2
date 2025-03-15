#include <iostream>
#include <string>
#include <thread>
using namespace std;

// creating chopstick semaphores
int chopstick[5] = { 1,1,1,1,1 };


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

void philo_process(int id)
{
    string eating = "Philosopher nr. " + to_string(id + 1) + " is eating.\n";
    string thinking = "Philosopher nr. " + to_string(id + 1) + " is thinking.\n";

    do {
        //philosopher waits for both chopsticks he needs
        wait(chopstick[id]);
        wait(chopstick[(id + 1) % 5]);
        cout << eating;
        this_thread::sleep_for(std::chrono::seconds(2)); //philosopher takes his time eating

        //philosopher signals he is done eating and the chopsticks are free
        signal(chopstick[id]);
        signal(chopstick[(id + 1) % 5]);
        cout << thinking;
        this_thread::sleep_for(std::chrono::seconds(2)); //philosopher takes his time thinking
    } while (true); //because the only thing the philosopher can do is either think or eat forever
}

int main()
{
    // creating philosopher threads and assigning them their function
    thread philo1(philo_process, 0);
    thread philo2(philo_process, 1);
    thread philo3(philo_process, 2);
    thread philo4(philo_process, 3);
    thread philo5(philo_process, 4);

    while (true) {} //so the program doesn't end
    return 0;
}