#same voltage different temperature
from collections import Counter

class measurment():
    def __init__(self):
        self.temperture = 0
        self.path = ''
        self.challenge = ''
        self.raw_data = []
        self.lines = 0
        self.is_gold = False
    def setup(self,path,temp='',challenge=''):
        tmp = [] #check golden error data
        self.temperture = temp
        self.path = path
        self.challenge = challenge
        file_name = 'test.txt'

        self.file_path =  self.path + file_name

        if '25' in self.file_path:
            self.is_gold = True
        rf = open(self.file_path,'r')

        for l in rf.readlines()[6:]:
            data = l.split()
            if (data[4] == '1'):
                data[1] = bin(int(data[1],16))[2:].zfill(8)
                if (data[1] != '00000000'): #withdraw <00> data
                    self.raw_data.append(data)
        if (self.is_gold == True):
            self._setGold()

        self.lines =  (len(self.raw_data))

    def _setGold(self):
        gold = Counter(x[1] for x in self.raw_data).most_common(1)[0][0] #'11111001'
        raw_data = [x[1] for x in self.raw_data]

        for i in range (len(self.raw_data)):
            self.raw_data[i][1] = gold


class analyze():
    def __init__(self):
        self.data_temp = []
        self.meas_array = []
        self.gold_data = []
        self.error_data_store = []

        self.group = 0

        self.len_array = 0
        self.min_value = 1000000 #inital value

        self.cnt_time = 0

        self.BER = 0 #BER = error_bit/ (8bit*min_value*group)
        self.store_path = ''

    def add_data(self,data=measurment()):
        min_value = data.lines
        self.data_temp.append(data.temperture)
        if (min_value < self.min_value):
            self.min_value = min_value #renew min value

        if (data.is_gold):
            self.gold_data = data
            self.store_path = data.path
            # print (data.raw_data[1] )
        else:
            self.meas_array.append(data)
            self.len_array = len(self.meas_array)
    def result(self):
        self.len_array = len(self.meas_array)

        error_bit_sum = 0
        self.error_bit = []#each temperature
        gold_data = self.gold_data

        comp_bit = '00000000'
        gold_bit = '00000000'

        # print (gold_data.raw_data)
        for comp_data in self.meas_array:
            tmp = 0
            for i in range (self.min_value):
                comp_bit = (comp_data.raw_data[i][1])
                gold_bit = (gold_data.raw_data[i][1])
                for j in range(len(gold_bit)): #div 11111001 as 1 1 1 1 1 0 0 1
                    if(gold_bit[j] != comp_bit[j]):
                        self.error_data_store.append(comp_bit)
                        print (comp_bit)
                        error_bit_sum += 1
                        tmp += 1
            print (tmp)
            self.error_bit.append(tmp)
        print (error_bit_sum)
        self.BER = error_bit_sum / (len(comp_bit) * (self.min_value) * (len(self.meas_array) + 1))
        print(self.BER)
        print (self.len_array)
        self.write_out()
    def write_out(self):
        path = self.store_path + 'result_v.txt'

        with open (path,'w') as wf:
            wf.write('#Begin:')
            wf.write(str(self.gold_data.challenge)+ str(self.min_value) +'\t')
            wf.write('Bit Error Rate: '+str(self.BER)+ '\n')
            for i in range (len(self.meas_array)):
                wf.write('Temperature: '+str(self.meas_array[i].temperture)+' : ')
                wf.write(str(self.error_bit[i])+'\n')

def main():
    current_dir = 'Thermal/chip1/'
    Temperature = ['0','10','25','40','55','70','85','100']

    file_path = []
    meas_array = []

    challenge = 'c1/'

    for i in Temperature:
        file_path.append(current_dir+i+'/1_2v/'+challenge)

    result = analyze()

    for i in range(len(file_path)):
        meas_array.append(measurment())
        meas_array[i].setup(file_path[i],Temperature[i],challenge)
        result.add_data(meas_array[i])
    # result.min_value = 1200
    result.result()
    print (result.min_value)

    # print (m1.lines)

if __name__ == '__main__':
    main()