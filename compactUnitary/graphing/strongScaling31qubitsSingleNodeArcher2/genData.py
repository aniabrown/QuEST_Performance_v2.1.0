import csv
import math

fileNameOutput = 'strongScaling31qubit.csv'

threads = [8, 16, 32, 64, 128]
ranks = 1
compareThread = 8
qubit = 30

getHeader = 1
fullTable = []
compareTime=1

for thread in threads:
    fileName = '../../archer2/singleNode/31qubits' + str(ranks) + 'nodes1ranks' + str(thread) + \
            'threads/TIMING_STATS_ROTATE_31qubits_CPU_' + str(ranks) + 'ranksx' + str(thread) + 'threads.csv'

    try:
        with open(fileName) as csvFileIn:
            reader = list(csv.reader(csvFileIn))
            if (getHeader):
                headers = ['numRanks', 'numThreads', 'speedup', 'speedupStandardDev', 'inverseTime'] + reader[0]
                fullTable.append(headers)
                getHeader = 0

            if (thread==compareThread):
                compareTime = float(reader[1+qubit][1])
                compareStandardDev = float(reader[1+qubit][2])
          
            time = float(reader[1+qubit][1])
            inverseTime = 1.0/time
            speedup = compareTime/time

            standardDev = float(reader[1+qubit][2])

            speedupStandardDev = math.sqrt( (compareStandardDev/compareTime)**2 + \
                    (standardDev/time)**2 )

            dataRow = [ranks, thread, speedup, speedupStandardDev, inverseTime] + reader[1+qubit]
            fullTable.append(dataRow)
    except:
        compareThread = compareThread*2
        print('!! Skipped: ' + fileName)


with open(fileNameOutput, 'w') as csvFileOut:
    writer = csv.writer(csvFileOut)
    writer.writerows(fullTable)

print('Table printed to ' + fileNameOutput)
