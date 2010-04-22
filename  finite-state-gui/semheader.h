/**Common header file semheader.h **/

union semun 
{
	int val;
	struct semid_ds *buf;
	ushort *array;
};

void err_sys (char * str)
{
	printf("%s",str);
}

void err_quit (char *str)
{
	printf("%s",str);
	exit(1);
}

void create_sem(int *semid, key_t key)
{
	union semun semarg;
	*semid = semget(key, 1, (IPC_CREAT | 0666));
	if( *semid < 0)
		err_quit( "Unable to get a semaphore");
	semarg.val = 0;
	if(semctl(*semid, 0, SETVAL, semarg) == -1 )
		err_quit("Unable to initialize the semaphore");
}

void release_sem(int semid)
{
	union semun semarg;
	//printf( "Releasing semaphore %d\n", semid);
	if(semctl(semid, 0, IPC_RMID, semarg) == -1)
		err_quit("Unable to release the semaphore");
}

//Decrement semaphore.
void p( int semid)
{
	struct sembuf sb;
	sb.sem_num = 0;
	sb.sem_op = -1;
	sb.sem_flg = SEM_UNDO;
	if( semop( semid, &sb, 1) == -1 )
		err_quit("p operation failed");
	//printf("\nP operation complete: %d\n",semid);
}

//Increment semaphore.
void v( int semid)
{
	struct sembuf sb;
	sb.sem_num = 0;
	sb.sem_op = 1;
	sb.sem_flg = SEM_UNDO;
	if( semop( semid, &sb, 1) == -1 )
		err_quit("v operation failed");
	//printf("\nV complete: %d\n",semid);
}

int getSem(key_t theKey)
{
	int temp = semget(theKey, 1, 0);
	if(temp == -1)
		printf("Couldn't retrieve semaphore!\n");
	else
		return temp;
}
//End semheader.h

