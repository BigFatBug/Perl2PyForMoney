# coding=utf8
import re
import sys
import getopt


class Handler:
    def __init__(self, inputFile, outputFile, logFile, qua, lim, splice):
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.logFile = logFile
        self.qua = qua
        self.lim = lim
        self.read = 0
        self.pass_filter = 0
        self.splice = splice
        self.result = {
            'Unm': 0,
            'Mul': 0,
            'Spl': 0,
            'Low': 0,
            'Too': 0
        }

    def run(self):
        with open(self.outputFile, 'w') as outputDatas:
            with open(self.inputFile, 'r') as inputDatas:
                line = inputDatas.readline()
                while line:
                    self.read += 1
                    if (self.analysis(line.replace('\n', ''))):
                        outputDatas.write(line)
                        self.pass_filter += 1
                    line = inputDatas.readline()

        self.makeLog()

    # True表示未被pass filter，False表示没有
    def analysis(self, line):
        datas = line.split('\t')
        nhs = 0
        len = 0
        nmi = 0
        if datas[5] == '*':
            self.result['Unm'] += 1
            return False
        if int(datas[1]) > 2000:
            self.result['Mul'] += 1
            return
        temp = re.match(r'(\d+)[HS]', datas[5])
        if temp:
            for i in temp.groups():
                nhs += int(i)
        temp = re.match(r'(\d+)[MISH]', datas[5])
        if temp:
            for i in temp.groups():
                len += int(i)
        temp = re.match(r'MD:.:(.+)', datas[12]) or re.match(r'MD:.:(.+)', datas[13])
        if temp:
            mid = temp.group()
            mtemp = re.match(r'(\d+)D', datas[5])
            if mtemp:
                for mi in mtemp.groups():
                    re.sub(r'[ATCG]{%s}' % mi, '', mid)
                re.sub(r'\d+', '', mid)
                nmi = len(mid)

        if nhs / len > self.splice:
            self.result['Spl'] += 1
        elif int(datas[4]) < self.qua:
            self.result['Low'] += 1
        elif nmi > self.lim:
            self.result['Too'] += 1
        else:
            return True
        return False

    def makeLog(self):
        with open(self.logFile, 'w') as outputDatas:
            outputDatas.write(
                "Total_reads\t%s\t100%%\nPass_filter\t%s\t%s%%\nUnmapped\t%s\t%s%%\nMultiple_mapped\t%s\t%s%%\nSplice\t%s\t%s%%\nLow_map_quality\t%s\t%s%%\nToo_much_mismatch\t%s\t%s%%\n" % (
                self.read, self.pass_filter, self.pass_filter / self.read * 100, self.result['Unm'],
                self.result['Unm'] / self.read * 100, self.result['Mul'], self.result['Mul'] / self.read * 100, self.result['Spl'],
                self.result['Spl'] / self.read * 100, self.result['Low'], self.result['Low'] / self.read * 100, self.result['Too'],
                self.result['Too'] / self.read * 100))


def main(argv):
    inputFile = 'test.bwa.sam'
    outputFile = 'test.q.sam'
    logFile = 'log'
    qua = 5
    lim = 5
    splice = 0.1
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
        for opt, arg in opts:
            if opt == '-h':
                print('input param: -i <inputfile> -o <outputfile> -l <logfile>')
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputFile = arg
            elif opt in ("-o", "--ofile"):
                outputFile = arg
            elif opt in ("-l", "--lfile"):
                logFile = arg
            elif opt in ("--qua", "-Q"):
                qua = int(arg)
            elif opt in ("--lim", "-L"):
                lim = int(arg)
            elif opt in ("--splice", "-S"):
                splice = float(arg)
    except Exception as e:
        print(e)
        # sys.exit(2)
    Handler(inputFile, outputFile, logFile, qua, lim, splice).run()

if __name__ == '__main__':
    main(sys.argv)