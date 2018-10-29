#include <thread>
#include <iostream>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string>
#include <cstring>
#include <algorithm>
#include <signal.h>
#include <sqlite3.h>

#define EXIT 0
#define ERROR -1
#define PWD -2

void run();
int	cReceive(int sock);
int cSend(int sock);
void setup(int sock); //user default is living ghost
void terminate(int signal);

int main(){
	signal(SIGINT, terminate);
	run();
	return EXIT_FAILURE; // correct exit from run
}

void setup(int sock){
	char username[64];
	int tries = 0;
	char password[64] = "", access_granted[64] = "BOB";

	std::cout << "\e[4mUsername:\e[0m ";
	std::cin.getline(username, sizeof(username));
	if(strcmp(username, "") == 0) strcpy(username, "Living Ghost");

	while(strcmp(access_granted, password) != 0){
		if(tries++ == 3) terminate(PWD);
		std::cout << "\e[4mPassword:\e[0m ";
		std::cin.getline(password, sizeof(password));

	}
	//std::cout << "\e[1;91mWelcome to BOB Server\e[0m\n";
	send(sock, username, strlen(username), 0);
}

void terminate(int signal = ERROR){
	switch(signal){
		case EXIT:
			std::cout << "\e[1;91m\nCu l8r M8!\e[0m\n" << "\e[1mdisconnected\e[0m\n"; break;
		case PWD:
			std::cout << "Too many incorrect tries.\n" << "\e[1moperation aborted\e[0m\n"; break;
		case ERROR:
			std::cout << "An error occured, sad...\n" << "\e[1moperation aborted\e[0m\n"; break;
	}
	exit(EXIT_SUCCESS);
}

void run(){
	struct sockaddr_in server;
	int sock = socket(AF_INET, SOCK_STREAM, 0);

	server.sin_family = AF_INET; // IPv4 address
	server.sin_addr.s_addr = inet_addr("164.132.196.204"); // Server IP
	//server.sin_addr.s_addr = inet_addr("0.0.0.0");
	server.sin_port = htons(10002); // Server Port - Host TO Network Short conversion

	if(sock == ERROR){
		perror("Error opening stream socket\n");
		terminate();
	}
	if(connect(sock, (struct sockaddr *) &server, sizeof(server)) == ERROR){
		perror("Error connecting to server\n");
		terminate();
	} else {
		std::cout << "\e[1mconnected\e[0m\n";
	}
	setup(sock);

	std::thread t1(&cReceive, sock);
	std::thread t2(&cSend, sock);
	
	t1.join();
	t2.join();
}

int cSend(int sock){
	char message[1024], serv_reply[1024];
	while (true){
		std::fill(message, message+1024, 0);
		std::fill(serv_reply, serv_reply+1024, 0);
		std::cin.getline(message, 1024);
		if(strcmp(message, "EXIT") == 0) terminate(EXIT);
		if(send(sock, message, strlen(message), 0) == ERROR){
			std::cout << "Erreur, message non envoyé!\n";
			return 1;
		} else {
			std::cout << "\033[1;32mmessage sent\033[0m\n\n";
		}
	}
}

int cReceive(int sock){
	char message[1024], serv_reply[1024];
	while (true){
		std::fill(message, message+1024, 0);
		std::fill(serv_reply, serv_reply+1024, 0);
		if (recv(sock, serv_reply, 1024, 0) < 0){
			std::cout << "Recu raté!\n";
			return 1;
		}	
		std::cout << "\e[1;2m" << serv_reply << "\e[0m" << "\n";
	}
}
