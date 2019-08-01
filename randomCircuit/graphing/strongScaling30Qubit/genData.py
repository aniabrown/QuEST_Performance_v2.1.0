import csv

fileNameOutput = 'strongScaling30qubit.csv'

ranks = [1, 2, 4, 8, 16, 32, 64]
threads = 16
compareRank = 1

getHeader = 1
fullTable = []
compareTime=1

for rank in ranks:
    fileName = '../../arcus-b_CPU/30qubits' + str(rank) + 'ranks' + str(threads) + \
            'threads/TIMING_STATS_ROTATE_30qubits_CPU_' + str(rank) + 'ranksx' + str(threads) + 'threads.csv'

    try:
        with open(fileName) as csvFileIn:
            reader = list(csv.reader(csvFileIn))
            if (getHeader):
                headers = ['numRanks', 'numThreads', 'speedup'] + reader[0]
                fullTable.append(headers)
                getHeader = 0

            if (rank==compareRank):
                compareTime = reader[1][1]
           
            speedup = float(compareTime)/float(reader[1][1])
            dataRow = [rank, threads, speedup] + reader[1]
            fullTable.append(dataRow)
    except:
        compareRank = compareRank*2
        print('!! Skipped: ' + fileName)


with open(fileNameOutput, 'w') as csvFileOut:
    writer = csv.writer(csvFileOut)
    writer.writerows(fullTable)

print('Table printed to ' + fileNameOutput)
