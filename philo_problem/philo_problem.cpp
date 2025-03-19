#include <iostream>
#include <string>
#include <thread>
using namespace std;

//making a pointer for chopstick array global
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

void philo_process(int id)
{
    string eating = "Philosopher nr. " + to_string(id + 1) + " is eating.\n";
    string thinking = "Philosopher nr. " + to_string(id + 1) + " is thinking.\n";

    do {
        //philosopher waits for both chopsticks he needs
        wait(chopstick[id]);
        wait(chopstick[(id + 1) % 5]);
        cout << eating;
        this_thread::sleep_for(chrono::seconds(2)); //philosopher takes his time eating

        //philosopher signals he is done eating and the chopsticks are free
        signal(chopstick[id]);
        signal(chopstick[(id + 1) % 5]);
        cout << thinking;
        this_thread::sleep_for(chrono::seconds(2)); //philosopher takes his time thinking
    } while (true); //because the only thing the philosopher can do is either think or eat forever
}

int main()
{
    int philo_num;
    cout << "Enter the number of philosophers: ";
    cin >> philo_num;

    //creating chopstick semaphores dynamically
    chopstick = new int[philo_num];
    for (int i = 0; i < philo_num; i++)
    {
        chopstick[i] = 1; //all chopsticks are available at first
    }


    //creating philosopher threads dynamically
    thread* philosophers = new thread[philo_num];
    for (int i = 0; i < philo_num; i++)
    {
        philosophers[i] = thread(philo_process, i);
    }

    while (true) {} //so the program doesn't end
    return 0;
}