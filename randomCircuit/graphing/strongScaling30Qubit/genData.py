import csv

fileNameOutput = 'strongScaling30qubit.csv'

ranks = [64, 32, 16, 8, 4, 2, 1]
threads = 16

getHeader = 1
fullTable = []

for rank in ranks:
    fileName = '../../arcus-b_CPU/30qubits' + str(rank) + 'ranks' + str(threads) + \
            'threads/TIMING_STATS_ROTATE_30qubits_CPU_' + str(rank) + 'ranksx' + str(threads) + 'threads.csv'

    try:
        with open(fileName) as csvFileIn:
            reader = list(csv.reader(csvFileIn))
            if (getHeader):
                headers = ['numRanks', 'numThreads'] + reader[0]
                fullTable.append(headers)
                getHeader = 0

            dataRow = [rank, threads] + reader[1]
            fullTable.append(dataRow)
    except:
        print('!! Skipped: ' + fileName + '. File not found.')


with open(fileNameOutput, 'w') as csvFileOut:
    writer = csv.writer(csvFileOut)
    writer.writerows(fullTable)

print('Table printed to ' + fileNameOutput)
