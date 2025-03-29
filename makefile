default: philo_program

philo_program: philo_problem/main.o
	g++ -Wall -Wextra -std=c++11 -o philo_problem/philo_program philo_problem/main.o

philo_problem/main.o: philo_problem/main.cpp
	g++ -Wall -Wextra -std=c++11 -c philo_problem/main.cpp -o philo_problem/main.o

clean:
	rm -f philo_problem/main.o philo_problem/philo_program