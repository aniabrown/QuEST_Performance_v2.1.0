import csv
import math

fileNameOutput = 'strongScaling30qubit.csv'

ranks = [8, 16, 32, 64, 128, 256]
threads = 128
compareRank = 8

getHeader = 1
fullTable = []
compareTime=1

for rank in ranks:
    fileName = '../../archer2/30qubits' + str(rank) + 'nodes1ranks' + str(threads) + \
            'threads/TIMING_STATS_ROTATE_30qubits_CPU_' + str(rank) + 'ranksx' + str(threads) + 'threads.csv'

    try:
        with open(fileName) as csvFileIn:
            reader = list(csv.reader(csvFileIn))
            if (getHeader):
                headers = ['numRanks', 'numThreads', 'speedup', 'speedupStandardDev', 'inverseTime'] + reader[0]
                fullTable.append(headers)
                getHeader = 0

            if (rank==compareRank):
                compareTime = float(reader[1][1])
                compareStandardDev = float(reader[1][2])
          
            time = float(reader[1][1])
            inverseTime = 1.0/time
            speedup = compareTime/time

            standardDev = float(reader[1][2])

            speedupStandardDev = math.sqrt( (compareStandardDev/compareTime)**2 + \
                    (standardDev/time)**2 )

            dataRow = [rank, threads, speedup, speedupStandardDev, inverseTime] + reader[1]
            fullTable.append(dataRow)
    except:
        compareRank = compareRank*2
        print('!! Skipped: ' + fileName)


with open(fileNameOutput, 'w') as csvFileOut:
    writer = csv.writer(csvFileOut)
    writer.writerows(fullTable)

print('Table printed to ' + fileNameOutput)
