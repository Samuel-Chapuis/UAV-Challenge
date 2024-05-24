#include <thread>
#include <iostream>
#include <mutex>

#include "../include/Task2.h"
#include "../include/Task1.h"
int main()
{
    std::thread t1( [] () {
		task1();
	});
	std::thread t2( [] () {
		task2();
	});

	t1.join();
	t2.join();

	std::cout << "Both tasks have completed.\n";
    system("PAUSE");
    return 0;
}

