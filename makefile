default: philo_program

philo_program: main.o
	g++ -Wall -Wextra -std=c++11 -o philo_program main.o

main.o: main.cpp
	g++ -Wall -Wextra -std=c++11 -c main.cpp -o main.o

clean:
	rm -f main.o philo_program