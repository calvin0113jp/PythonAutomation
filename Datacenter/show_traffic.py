# The file is used for traffic of dynamic show

# For ubuntu 18.04 install
#1. sudo apt-get install tk-dev
#2. sudo apt-get install python-tk

#Example
#Demo with client : iperf / ib_write_bw
#script: start.traffic.sh in the PC

#Demo 6 client


import datetime
import time
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#----General setting----


#-----------------------

#create plot 
#Decreasing graph
def get_iperf_sum(logfile):
    # capture iperf result

    global iperf_sum

    with open ('%s' %logfile , 'r') as f:
        line = f.read()

    iperf_sum_list = re.findall("SUM]\s+\d+.\d+-\s*\d+.\d+\s\w+\s+\d+.\d+\sGBytes\s+(\d+.\d+\s)Gbits" , line)

    #iperf_sum = iperf_sum_list[:-11:-1]
    #iperf_sum.sort()
    
    iperf_sum = iperf_sum_list[:-2:-1]#capture the last position
    print (iperf_sum)
    
    return iperf_sum

    
def get_ib_write_sum(logfile):
    # capture ib_write_bw of bandwidth
    global ib_write_sum

    with open ('%s' %logfile ,'r') as f:
        line1 = f.read()

    ib_write_sum_list = re.findall("0.00\s+(\d+.\d+)" , line1)

    #ib_write_sum = ib_write_sum_list[:-11:-1]
    #ib_write_sum.sort()

    ib_write_sum = ib_write_sum_list[:-2:-1]#capture the last position
    print (ib_write_sum)

    return ib_write_sum

# create_plot_bar
def create_plot():

    plt.ion() #interactive mode
    #plt.figure(1)

    for i in range(3600): # for 1 hour
        
        #Which traffic do you used
        get_iperf_sum(logfile='pc2.log')
        get_iperf_sum(logfile='pc3.log')
        get_iperf_sum(logfile='pc4.log')
        get_iperf_sum(logfile='pc5.log')
        get_ib_write_sum(logfile='pc6.log')
        

        plt.clf()
        

        #x = [datetime.datetime.now() + datetime.timedelta(seconds=i) for i in range(len(iperf_sum))]
        x = [datetime.datetime.now() + datetime.timedelta(seconds=i) for i in range(10)]
        plt.plot(x,iperf_sum, 's-',color = 'r',label="PC2-iperf")

        #x = [datetime.datetime.now() + datetime.timedelta(seconds=i) for i in range(len(ib_write_sum))]
        x = [datetime.datetime.now() + datetime.timedelta(seconds=i) for i in range(10)]
        plt.plot(x,ib_write_sum, 's-',color = 'b',label="PC3-iperf")

        x = [datetime.datetime.now() + datetime.timedelta(seconds=i) for i in range(10)]
        plt.plot(x,ib_write_sum, 's-',color = 'b',label="PC4-iperf")

        x = [datetime.datetime.now() + datetime.timedelta(seconds=i) for i in range(10)]
        plt.plot(x,ib_write_sum, 's-',color = 'b',label="PC5-iperf")

        x = [datetime.datetime.now() + datetime.timedelta(seconds=i) for i in range(10)]
        plt.plot(x,ib_write_sum, 's-',color = 'b',label="PC6-ib")
        
        plt.title("Mellanox ConnectX-6 Traffic Graph")
        plt.ylabel("Speed - Gbit/s")
        plt.xlabel("Time")

        #plt.ioff()
        plt.xticks(x,rotation=0)
        plt.grid(True) 

        # beauty the x-labels and time format to h:m
        plt.gcf().autofmt_xdate()
        myFmt = mdates.DateFormatter('%H:%M:%S')
        plt.gca().xaxis.set_major_formatter(myFmt)
        plt.legend(loc='upper left')

        # disaply data for 5 sec
        plt.draw()
        plt.pause(5)
        #plt.show()

def create_plot_bar(loop,refresh):

    plt.ion() #interactive mode

    for i in range(loop):
        plt.clf()
        
        # get log
        pc2 = ''.join(get_iperf_sum(logfile='pc2.log'))
        pc3 = ''.join(get_iperf_sum(logfile='pc3.log'))
        pc4 = ''.join(get_iperf_sum(logfile='pc4.log'))
        pc5 = ''.join(get_iperf_sum(logfile='pc5.log'))
        pc6 = ''.join(get_ib_write_sum(logfile='pc6.log'))
    
        # transfer the log and output
        pc_result = []
        pc_result.append(pc2)
        pc_result.append(pc3)
        pc_result.append(pc4)
        pc_result.append(pc5)
        pc_result.append(pc6)
        pc_result = list(map(lambda x:float(x), pc_result)) # list str to value
        print (pc_result)

        # Display the drop packets of percentage
        
        

        client = ['pc2','pc3','pc4','pc5','pc6']
        c1 = '#99ccff'
        c2 = '#ccffff'
        c3 = '#6699cc'
        c4 = '#006699'
        c5 = '#003366'
    
        color_list = [c1,c2,c3,c4,c5]
        width = 0.4
        
        #drow pic1
        plt.subplot(231)
        plt.bar(range(5), pc_result, align = 'center', width=0.6 , color= color_list, alpha = 1) # 添加軸標籤

        plt.ylabel('Speed - Gbit/s') 
        plt.title('Mellanox ConnectX-6 Traffic Graph') # 添加刻度標籤 
        plt.xticks(range(5),client) # 設置Y軸的刻度範圍 
    
        #plt.ylim([200,100]) # 為每個條形圖添加數值標籤 
        for x,y in enumerate(pc_result):
            plt.text(x,y,'%s'%y,ha='center') 
        #plt.show()
        
        #drow pic2
        x = ['Drop Packets']
        pc_drop_packet = [3442.233]
        plt.subplot(232)
        plt.bar(x , pc_drop_packet , align = 'center' , width=0.4 , color= color_list , alpha = 1)

        plt.ylabel('Count x 1000')
        for x,y in enumerate(pc_drop_packet):
            plt.text(x,y,'%s'%y,ha='center')
        #plt.ylim(0, 300000)


        plt.draw()
        plt.pause(refresh)
        print ('Run for %s times' %i)

def test():
    x1 = [1,2,3,4,5]
    y1 = [2,6,8,7,9]
    y2 = [3,5,6,1,2]
    # 比起堆疊長條圖，分組長條圖稍微調整數據以達到效果
    width = 0.4 #先設定每個長條的寬度
    plt.bar([i-width/2 for i in x1], y1, width=width, label='G1') #注意這裡的X軸座標為x1中的數據減去寬度的一半
    plt.bar([i+width/2 for i in x1], y2, width=width, label='G2') #注意這裡的X軸座標為x1中的數據加上寬度的一半
    plt.legend()
    plt.show()


if __name__=='__main__':

    #create_plot()
    create_plot_bar(loop=3600,refresh=5)
    #test()





