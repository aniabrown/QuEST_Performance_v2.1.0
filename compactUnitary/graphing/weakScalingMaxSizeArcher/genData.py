import csv
import math

fileNameOutput = 'weakScalingMaxSizeArcher.csv'

ranks = [2, 4, 8, 16, 32, 64]
qubits= [31, 32, 33, 34, 35, 36]
threads = 24
compareRank = 1

getHeader = 1
fullTable = []
compareTime=1

for index in range(len(ranks)):
    rank = ranks[index]
    qubitSize = qubits[index]
    fileName = '../../archer/' + str(qubitSize) +'qubits' + str(rank) + 'ranks' + str(threads) + \
            'threads/TIMING_STATS_ROTATE_' + str(qubitSize) + 'qubits_CPU_' + str(rank) + 'ranksx' + str(threads) + 'threads.csv'

    try:
        with open(fileName) as csvFileIn:
            reader = list(csv.reader(csvFileIn))
            if (getHeader):
                headers = ['numRanks', 'numThreads', 'speedup', 'speedupStandardDev'] + reader[0]
                fullTable.append(headers)
                getHeader = 0

            #print(reader)
            time = float(reader[1][1])

            print(time)

            standardDev = float(reader[1][2])

            dataRow = [rank, threads, time, standardDev] + reader[1]
            fullTable.append(dataRow)
    except:
        compareRank = compareRank*2
        print('!! Skipped: ' + fileName)


with open(fileNameOutput, 'w') as csvFileOut:
    writer = csv.writer(csvFileOut)
    writer.writerows(fullTable)

print('Table printed to ' + fileNameOutput)
