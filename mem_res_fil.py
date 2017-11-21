# coding=utf8
import re
import sys
import getopt

class Handler:

    def __init__(self, inputFile, outputFile, qua, lim, splice):
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.qua = qua
        self.lim = lim
        self.splice = splice
        self.result = {}
        self.inf = {}

    def run(self):
        with open(self.inputFile, 'r') as inputDatas:
            line = inputDatas.readline()
            while line:
                self.analysis(line.replace('\n', ''))
                line = inputDatas.readline()

    def analysis(self, line):
        datas = line.split('\t')
        nhs = 0
        len = 0
        nmi = 0
        if datas[5] == '*':
            self.inf[datas[0]] = 'Unm'
            return
        if int(datas[1]) > 2000:
            self.result['Mul'] = self.result.setdefault('Mul', 0) + 1
            return
        temp = re.match('(/d+)[HS]', datas[5])
        if temp:
            for i in temp.groups():
                nhs += int(i)
        temp = re.match('(/d+)[MISH]', datas[5])
        if temp:
            for i in temp.groups():
                len += int(i)
        temp = re.match('MD:.:(.+)', datas[12])
        if temp:
            mid = temp.group()
            mtemp = re.match('(\d+)D', datas[5])
            if mtemp:
                for i in mtemp:
                   mid.replace('')




def main(argv):
   inputfile = ''
   outputfile = ''
   logfile = ''
   qua = 5
   lim = 5
   splice = 0.1
   try:
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    for opt, arg in opts:
        if opt == '-h':
         print ('input param: -i <inputfile> -o <outputfile> -l <logfile>')
         sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-l", "--lfile"):
            logfile = arg
        elif opt in ("--qua", "-Q"):
            qua = int(arg)
        elif opt in ("--lim", "-L"):
            lim = int(arg)
        elif opt in ("--splice", "-S"):
            splice = float(arg)
   except:
      print(e)
      sys.exit(2)