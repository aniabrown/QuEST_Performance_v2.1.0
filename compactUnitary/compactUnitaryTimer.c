/** @file timingDemo.c
 * Measure execution time for rotations of qubits.
 * An example using the QuEST library
 */

// ==================================================================== //
//                                                                      //
//  demo.c -- qubit operarion demonstrator for QuEST                    //
//                                                                      //
// ==================================================================== //

# include <stdio.h>
# include <stdlib.h>
# include <time.h>
# include <math.h>
# include <unistd.h>
# include <string.h>
# include <omp.h>

# include "QuEST_precision.h"
# include "QuEST.h"

# define maxNumQubits 40
//! Number of times rotations are repeated for timing purposes
//! 1: perform one rotation outside the timing loop to get around long communication
//! time for first MPI send/recv
# define INIT_COMMUNICATION 1

const long qreal Pi = 3.14159265358979323846264338327950288419716939937510;

# include <stdlib.h>
# include <sys/time.h>

// ==================================================================== //
//                                                                      //
//     system_timer -- precision walltime function, computes            //
//                     walltime based on the gettimeofday() function    //
//                                                                      //
// ==================================================================== //

qreal system_timer (void) {
    struct timeval time;
    gettimeofday (&time, NULL);
    return time.tv_sec + time.tv_usec / 1000000.0;
}

int system_timer_usec (void) {
    struct timeval time;
    gettimeofday (&time, NULL);
    return time.tv_sec*1000000 + time.tv_usec;
}

//--------------------------------------------------------------
//---------------------- START OF main()  ----------------------
//--------------------------------------------------------------
int main (int narg, char** varg) {

    QuESTEnv env;
    env = createQuESTEnv();

    // model vars
    int numQubits, numTrials;

    Qureg qureg; 
    qreal normError=0;

    // number of qubits is command line argument
    if (narg >= 2) {
        numQubits = atoi(varg[1]);
        if (numQubits < 1 || numQubits > maxNumQubits) {
            printf(" *** error: argument %d out of range (1 -- %d)\n", numQubits,maxNumQubits);
            exit (EXIT_FAILURE);
        }
        numTrials = atoi(varg[2]);
    } else {
        printf(" *** error: too few arguments, number of qubits expected\n");
        exit (EXIT_FAILURE);
    }


    // timing variables
    qreal wtime_start,
           wtime_stop, wtime_duration,
           app_wtime_stop, app_wtime_start;
    qreal *timingVec;
    int trial;

    app_wtime_start = system_timer();

    timingVec = (qreal*) malloc(numTrials*numQubits*sizeof(timingVec));
    
    qureg = createQureg(numQubits, env);

    if (env.rank==0){
        reportQuregParams(qureg);
        reportQuESTEnv(env);
    }

    // initialise the state to |0000..0>
    initZeroState(qureg);


    // prepare files for writing output state vector and timing data
    FILE *timing, *distribution;
    char envString[255];
    getEnvironmentString(env, qureg, envString);
    char filename[255];

    if (env.rank==0){  
        sprintf(filename, "TIMING_STATS_ROTATE_%s.csv", envString);
        timing = fopen(filename, "w");
        fprintf(timing, "qubit, time(s), standardDev, maxDelta, minDelta\n");

        sprintf(filename, "TIMING_FULL_ROTATE_%s.csv", envString);
        distribution = fopen(filename, "w");
        fprintf(distribution, "qubit, trials\n");
    }

    qreal ang1 = 1.2320;
    qreal ang2 = 0.4230; 
    qreal ang3 = -0.6523;

    Complex alpha, beta;
    alpha.real = cos(ang1) * cos(ang2);
    alpha.imag = cos(ang1) * sin(ang2);
    beta.real  = sin(ang1) * cos(ang3);
    beta.imag  = sin(ang1) * sin(ang3);

    // do a big MPI communication to get around first send/recv in the program occasionally taking many times longer
    //(due to MPI setup?)
    if (INIT_COMMUNICATION){
        compactUnitary(qureg,numQubits-1,alpha,beta);
    }


    for (int i=0; i<numQubits; i++) {
        if (env.rank==0) fprintf(distribution, "%d", i);
        for (trial=0; trial<numTrials; trial++){
            // for timing -- have all ranks start at same place
            syncQuESTEnv(env);
            wtime_start=system_timer();

            // do rotation of each qubit numTrials times for timing
            compactUnitary(qureg,i,alpha,beta);
            //printf("wtime duration %f\n", wtime_duration);

            syncQuESTEnv(env);
            wtime_stop=system_timer();
            wtime_duration=wtime_stop-wtime_start;
            if (env.rank==0) {
                timingVec[trial*numQubits + i]=wtime_duration;
                fprintf(distribution, ",%.8f", timingVec[trial*numQubits + i]);
                fflush(distribution);
            }
        }
        if (env.rank==0) fprintf(distribution, "\n");
    }

    if (env.rank==0) printf("Applied random circuit\n"); 
    // check vector size is unchanged
    normError=1.0-calcTotalProb(qureg);
    if (env.rank==0) printf("VERIFICATION: norm error = %e\n", normError);

    // report timing to file
    if (env.rank==0){
        qreal totTime, avg, standardDev, temp, max, min;
        for(int i=0; i<numQubits; i++){
            max=0; min=10e5;
            totTime=0;

            for (trial=0; trial<numTrials; trial++){
                temp=timingVec[trial*numQubits + i];
                totTime+=temp;
                if (temp<min) min=temp;
                if (temp>max) max=temp;
            }

            avg = totTime/(qreal)(numTrials);
            standardDev=0;
            for (int trial=0; trial<numTrials; trial++){
                    temp = timingVec[trial*numQubits + i]-avg;
                    standardDev += temp*temp;
            }
            standardDev = sqrt(standardDev/(qreal)(numTrials));

            fprintf(timing, "%d, %.8f, %.8f, %.8f, %.8f\n", i, avg, standardDev, max-avg, avg-min);
        }
    }

    // free memory
    if (env.rank==0) fclose(timing);
    if (env.rank==0) fclose(distribution);

    destroyQureg(qureg, env);

    if (env.rank==0) free(timingVec);

    destroyQuESTEnv(env);
    
    app_wtime_stop = system_timer();
    printf("Total program execution: %f s\n", (app_wtime_stop-app_wtime_start));

    return EXIT_SUCCESS;
}

