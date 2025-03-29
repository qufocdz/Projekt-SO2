philo_problem: philo_problem/philo_problem.cpp
	g++ -std=c++11 -Wall philo_problem/philo_problem.cpp -o philo_problem

clean:
	rm -f philo_problem
