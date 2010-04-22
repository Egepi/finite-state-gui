/***************************************************************
* Author: Todd Silvia
* CS 385, Spring 2010
* Program 2 - Broadcasting system
* Date: April 1st 2010
*
* write.c - This file is used to create all semaphores and shared
* memory used by the broadcasting project. It also recieves the
* messages as input from the user to broadcast to the readers.
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

int readInput();

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
* Main method responsible for overall function of write process.
*/
int main()
{
	printf("Author: Todd Silvia\nCS 385 Spring 2010");
	printf("\nProgram 2\nApril 1st 2010\n\n");

	/*Create semaphores*/
	create_sem(&reading_sem, reading_key);
	create_sem(&writing_sem, writing_key);
	printf("All semaphores created...\n");
	
	
	/*Create shared memory*/
	if((shmid = shmget(shm_key, SHMSZ, IPC_CREAT | 0666)) < 0)
	{
		perror("shmget");
	}
	printf("Created shared memory...\n");
	
	/*Attach writer process to shared memory */
	if((shm = shmat(shmid, NULL, 0)) == (char *)-1)
	{
		perror("shmat");
	}
	
	/*Waiting for reader processes to be ready*/
	printf("\nWaiting for reader processes to be ready.\n");
	p(writing_sem);
	p(writing_sem);
	printf("All readers are ready.\nPlease enter a message followed by return:");
	v(writing_sem);
	v(writing_sem);
	
	//Loop while broadcasting open
	while(readInput() == 1);
	
	printf("Waiting for both readers to close...\n");
	p(writing_sem);
	//p(writing_sem);
	
	//Detaching shared memory
	printf("Detaching shared memory...\n");
	if(shmdt(shm) == -1)
	{
		perror("shmdt");
		exit(1);
	}
	
	//Releasing Shared memory
	printf("Releasing shared memory...\n");
	if(shmctl(shmid, IPC_RMID, (struct shmid_ds *) NULL) == -1)
	{
		perror("shmctl");
		exit(1);
	}

	//Releasing all of the semaphores
	printf("Releasing all semaphores...\n");
	release_sem(reading_sem);
	release_sem(writing_sem);
	printf("\nProgram exiting...\n");
	return 0;
	
}

/***************************************************************
* Waits for both readers to signal the are ready to read. Then
* retrieves the message from the user and places it in shared 
* memory. 
*
* @Return: 0 if user enters "Quit" as message
*	    : else 1
*/
int readInput()
{
	//Wait for both readers to be done reading
	p(writing_sem);
	p(writing_sem);
	
	char msg[101];
	//Retrieve message from user input
	fgets(msg, sizeof msg, stdin);
	
	int counter = 0;
	tempShm = shm;
	//Loop to add user inputed message into shared memory
	for(counter; counter < sizeof msg; counter++)
	{
		*tempShm = msg[counter];
		tempShm++;
	}

	//Check if message was "Quit"
	if(strcasecmp(msg, "Quit\n") == 0)
	{
		*shm = '\0';
		v(reading_sem);
		v(reading_sem);
		return 0;
	}
	
	//Allow readers to no read message from shared memory
	v(reading_sem);
	v(reading_sem);
	return 1;
}
//End write.c

