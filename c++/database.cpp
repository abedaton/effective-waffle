#include <sqlite3.h>
#include <cstring>
#include <string.h>
#include <iostream>

char** usernameChecking;
char** passwordChecking;
char* tusername;
long tpassword;

int main();
void addUser(sqlite3* db, char* username, char* password);
void updatePassw(sqlite3* db, int age, char* username);
void createTable(sqlite3* db);
bool isLoginOk(sqlite3* db, char* username, char* password);
bool login = false;
long hashPass(char* password);
static int myCallback(void* NotUsed, int argc, char** argv, char** azColName);

extern "C"{
	void callMain(){
		main();
	}
}


void savelogininfo(char *user, char *pwd){
	std::cout<<*user<<std::endl;
	usernameChecking=(& user);
	passwordChecking= (&pwd);
}

static int callback(void* NotUsed, int argc, char** argv, char** azColName){
	int i;
	for (i = 0; i < argc; i++){
		printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
	}
	printf("\n");
	return 0;
}

int main(){
	sqlite3 *db;
	char *sql;
	int rc;
	// Open the test.db file
	rc = sqlite3_open(":memory:", &db);
	if(rc != SQLITE_OK){
		fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
	} else {
		fprintf(stderr, "Open database successfully\n");
	}

	createTable(db);

	addUser(db, "Machin", "123");
	addUser(db, "jeande", "abc");
	std::cout << isLoginOk(db, "Machin", "123") << std::endl;
	std::cout << isLoginOk(db, "jeande", "abc") << "\n";

    std::cout << "Heyoooo test! 42\n";
	std::cout << isLoginOk(db, "Machin", "a\" OR \"1\" = \"1") << "\n";
	//std::cout << isLoginOk(db, argv[1], argv[2]) << std::endl;

	sqlite3_close(db);

	return 0;
}

void createTable(sqlite3* db){
	// create users
	char* zErrMsg = 0;
	char* sql;
	int rc;
	sql = "CREATE TABLE users (username text, password BIGINT)";

	rc = sqlite3_exec(db, sql, callback, 0, &zErrMsg);

	if( rc == SQLITE_OK ) {
		std::cout << "New table created\n";
	} else {
		std::cout << "This table already exists !\n";
	}
	std::cout << "---------------------------------------------\n";
}


void addUser(sqlite3 *db, char *username, char *password){
	if (!db) return;
	sqlite3_stmt *stmt;
	const char *pzTest;

	// Insert data item into users
	char *sql = "INSERT INTO users (username, password) VALUES (?,?)";
	int rc = sqlite3_prepare(db, sql, strlen(sql), &stmt, &pzTest);

	if(rc == SQLITE_OK){
		char** temp = &username;
		char* addusername = *temp;
		std::cout << __LINE__ << " New username = " << addusername << std::endl;
		// Hash password
		long addpassword = hashPass(password);
		std::cout << __LINE__ << " New password " << password << " hashed " << addpassword << std::endl;
		// Bind the value
		sqlite3_bind_text(stmt, 1, addusername, strlen(addusername), 0);
		sqlite3_bind_int64(stmt, 2, addpassword);
		// Commit
		sqlite3_step(stmt);
		sqlite3_finalize(stmt);
		std::cout << __LINE__ << " User added\n" << "---------------------------------------------\n";
	}
}

long hashPass(char* password){
	std::string spassword = password;
	std::hash<std::string>hashFct;
	return hashFct(spassword);
}

bool isLoginOk(sqlite3* db, char* username, char* password){
	char* zErrMsg = 0;
	char** temp = &username;
	tusername = *temp;
	tpassword = hashPass(password);
	
	std::string ssql = std::string("SELECT * FROM users WHERE username = '") + username + "' AND password = " + std::to_string(tpassword);

	char sql[ssql.size()+1];
	strcpy(sql, ssql.c_str());
	int rc = sqlite3_exec(db, sql, myCallback, 0, &zErrMsg);
	if (rc != SQLITE_OK) {
		exit(1);
	}

	if(login == false) {
		std::cout << "Wrong username or password\n";
		return false;
	} else{
		std::cout << __LINE__ << " Login is OK\n";
		login = false;
	}

	return true;
}

static int myCallback(void* NotUsed, int argc, char** argv, char** azColName){
	std::cout << __LINE__ << " Username check/serv "<< argv[0] << std::endl;
	std::cout << __LINE__ << " Password check/serv "<< argv[1] << std::endl;


	if(strcmp(argv[0], tusername) == 0 && atol(argv[1]) == tpassword){
		login = true;
	} else { 
		login = false;
	}
	return 0;
}











//void updatePassw(sqlite3 *db, int age, char *username){
//  if (!db)
//                return;
//
//  //char* zErrMsg = 0;
//  sqlite3_stmt* stmt;
//  const char* pzTest;
//  char* sql;
//
//  // Insert data item into users
//  sql = "UPDATE users SET password = ? WHERE username = ?";
//
//  int rc = sqlite3_prepare(db, sql, strlen(sql), &stmt, &pzTest);
//
//  if( rc == SQLITE_OK ) {
//                // bind the value
//                sqlite3_bind_int(stmt, 1, age);
//                sqlite3_bind_text(stmt, 2, username, strlen(username), 0);
//
//                // commit
//                sqlite3_step(stmt);
//                sqlite3_finalize(stmt);
//  }
//}
