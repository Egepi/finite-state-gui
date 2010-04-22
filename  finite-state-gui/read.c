/***************************************************************
* Author: Todd Silvia
* CS 385, Spring 2010
* Program 2 - Broadcasting system
* Date: April 1st 2010
*
* read.c - This file waits for user to enter "Yes". Then the 
* process will attach to shared memory and shared semaphores 
* used concurrently with write.c process to ensure concurrency.
* Then the file keeps displaying messages in the terminal until
* the message "Quit" is recieved by the user.
***************************************************************/


#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <stdlib.h>
#include <sys/shm.h>
#include <string.h>
#include "semheader.h"

int canStart();
int readMSG();


/*Global Variables*/
int stopInt;
int SHMSZ = 100;
int reading_sem;
int writing_sem;
int shmid;
key_t reading_key = 4546;
key_t writing_key = 4548;
key_t shm_key = 1234;
char *shm, *tempShm;

/***************************************************************
* Main method responsible for overall function of read process.
*/
int main()
{
	printf("Author: Todd Silvia\nCS 385 Spring 2010");
	printf("\nProgram 2\nApril 1st 2010\n\n");
	
	//Loop until the user enters "Yes"
	printf("Accept messages from writer? ");
	while(canStart() == 0);
	
	//Attach read process to shared semaphores
	reading_sem = getSem(reading_key);
	writing_sem = getSem(writing_key);
	
	/* Locate the shared memory*/
	if((shmid = shmget(shm_key, SHMSZ, 0666)) < 0)
	{
		perror("shmget");
		exit(1);
	}
	
	/*Attach to shared memroy*/
	if((shm = shmat(shmid, NULL, 0)) == (char *) -1)
	{
		perror("shmat");
		exit(1);
	}
	v(writing_sem);
	
	//Looping until the message "Quit" is recieved
	while(readMSG() == 1);
	
	//"Quit" recieved so process closing
	printf("\n*****Broadcast session closed*****\n\n");
	printf("Detaching shared memory...\n");
	
	//Detaching shared memory
	if(shmdt(shm) == -1)
	{
		perror("shmdt");
		exit(1);
	}
	
	printf("Program exiting...\n");
	v(writing_sem);
	return 0;
}

/***************************************************************
* Checks if user enters "Yes" to inform the writer that this
* reader is read to accept messages.
*
* @Return: 1 if user entered "Yes"
*	    : 0 if user eneters not "Yes"
*/
int canStart()
{
	char startInput[4];
	scanf("%s", startInput);
	if(strcasecmp(startInput, "Yes") == 0)
	{
		printf("*****Broadcast session now open*****\n\n");
		return 1;
	}
	else
	{
		printf("Im sorry, are you ready to read messages? ");
		return 0;
	}
}

/***************************************************************
* Waits for semaphore to determine when able to read message from
* shared memory. Then reads the message from the shared memory and
* displays that message onto the screen.
*
* @Return: 0 if user had entered "Quit"
*        : else 1
*/
int readMSG()
{
	//Waiting for writer to to finish writing to shared memory
	p(reading_sem);
	
	char msg[101];
	int counter = 0;
	char temp;
	tempShm = shm;
	
	//Read message from the shared memory
	for(counter; counter <= sizeof msg; counter++)
	{
		msg[counter] = *tempShm;
		tempShm++;
	}
	
	//Check if the user had entered "Quit"
	if(msg[0] == '\0')
	{
		return 0;
	}
	
	//Print the message read from shared memory to the screen
	printf("%s", msg);
	v(writing_sem);
	return 1;
}

//End read.c
