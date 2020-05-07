#!/bin/bash

# set the number of nodes and processes per node. We are running one process on a single node
#SBATCH --nodes=32
#SBATCH --ntasks-per-node=1

#SBATCH --mem=50Gb
# uncomment if NUM_QUBITS - log2(NUM_NODES) > 30
####SBATCH --mem=100Gb

# set max wallclock time
#SBATCH --time=05:00:00

# set name of job
#SBATCH --job-name QuEST-network

# set queue
# Remove this line for runs that are not part of the nqit reservation
##SBATCH --reservation=nqit

module purge
module load mvapich2/2.1.0__intel-2016
module load cmake/3.8.0

export KMP_AFFINITY=disabled
export OMP_NUM_THREADS=16


. enable_arcus-b_mpi.sh

CMAKE_OPTIONS="-DUSER_SOURCE='compactUnitaryTimer.c' -DQuEST_DIR=QuEST_v2.1.0 -DDISTRIBUTED=1"

rm -r build
mkdir build; cd build
cmake $CMAKE_OPTIONS ../../..
make

NUM_QUBITS=35
NUM_TRIALS=50
EXE=demo

time mpirun $MPI_HOSTS ./$EXE $NUM_QUBITS $NUM_TRIALS

cp TIMING* ..

