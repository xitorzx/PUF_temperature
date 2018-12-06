def comp (a='00000000',b='11111111'):
    leng = len(a)
    cnt = 0
    for index in range (leng):
        if (a[index] != b[index]):
            cnt = cnt + 1
    return cnt

class measurement():
    def __init__(self):
        self.path = ''
        self.raw_data = []
        self.data = []
        self.times = 0
    def setup(self,path,file_name):
        self.path = path
        self.file_name = file_name

        file_path = path+file_name+'.txt'

        rf = open(file_path,'r')
        cnt = 0
        for l in rf.readlines()[6:]:
            data = l.split( )
            if (data[4] == '1'): #temperary: 1111_1111 may occur in odd or even number. initial odd number
                self.raw_data.append(data)
        self.write_out()
    def write_out(self):
        file_path =self.path + self.file_name + '_out.txt'
        with open(file_path,'w') as file:
            for i in self.raw_data:
                new_str = (' '.join(i[1]))
                self.data.append(new_str)
                file.write('%s \n'%new_str)


class analyze():
    def __init__(self,data1=['00000000'],data2=['00000000'],data3=['00000000'],data4=['00000000'],data5=['00000000'],data6=['00000000'],f_path='/'):
        self.max_value = 1000
        self.gold_data = data4
        self.exp_data = []

        self.f_path = f_path

        self.exp_data.append(data1) #0.9v
        self.exp_data.append(data2) #1.0v
        self.exp_data.append(data3) #1.1v
        # self.exp_data.append(data4) set as golden pattern
        self.exp_data.append(data5) #1.3v
        self.exp_data.append(data6) #1.4v

        self.error_bit = []
        self.error_data = [[] for x in range(5)]
    def comparsion(self):
        tmp_error_bit = 0

        error_bit = 0
        which_data = 0
        for data in self.exp_data: #for data1~data6
            for index in range(self.max_value): #total 1000 datas
                gold = self.gold_data[index]
                item = data[index]
                tmp_error_bit = error_bit
                for i in range (len(gold)):
                    if (gold[i] != item[i]):
                        error_bit += 1
                if tmp_error_bit != error_bit:
                    self.error_data[which_data].append(item)

            self.error_bit.append(error_bit)
            error_bit = 0
            which_data +=1
        print (self.error_data)
        print (self.error_bit)
    def summary(self):
        path = self.f_path + 'output.txt'
        with open (path,'w') as wf:
            wf.write('index: error_bit: error_rate: error_data:\n')
            for index in range (5):
                message = str(index) + ' :' + str(self.error_bit[index])+' :'+ str(self.error_bit[index]/8/1000)+' :'
                wf.write(message)
                for i in self.error_data[index]:
                    wf.write(str(i)+', ')
                wf.write('\n')

def main():
    current_dir = 'Jess_Chips'
    chips = '/chip1/c1/'
    f_path = current_dir + chips
    ms1 = measurement()
    ms1.setup(f_path,'0v9')
    ms2 = measurement()
    ms2.setup(f_path,'1v')
    ms3 = measurement()
    ms3.setup(f_path,'1v1')
    ms4 = measurement()
    ms4.setup(f_path,'1v2')
    ms5 = measurement()
    ms5.setup(f_path,'1v3')
    ms6 = measurement()
    ms6.setup(f_path,'1v4')

    ana = analyze(ms1.data, ms2.data, ms3.data, ms4.data, ms5.data, ms6.data, f_path)
    ana.comparsion()
    ana.summary()

if __name__ == '__main__':
    main()