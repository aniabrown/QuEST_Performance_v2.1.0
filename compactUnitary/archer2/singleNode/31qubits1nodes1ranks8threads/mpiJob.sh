#!/bin/bash

#SBATCH --job-name=QuEST
#SBATCH --time=4:30:0
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=8

#SBATCH --account=y18
#SBATCH --partition=standard
#SBATCH --export=none
#SBATCH --qos=standard

module load epcc-job-env
module restore PrgEnv-gnu
#module restore /etc/cray-pe.d/PrgEnv-gnu

export OMP_NUM_THREADS=8
export OMP_PLACES=cores

CMAKE_OPTIONS="-DUSER_SOURCE='compactUnitaryTimer.c' -DQuEST_DIR=QuEST_v2.1.0-gcc10Patch -DDISTRIBUTED=1 -DTESTING=0"

rm -r build
mkdir build; cd build
cmake $CMAKE_OPTIONS ../../../..
make

NUM_QUBITS=31
NUM_TRIALS=50
EXE=demo

srun --hint=nomultithread --distribution=block:block ./$EXE $NUM_QUBITS $NUM_TRIALS

cp TIMING* ..

