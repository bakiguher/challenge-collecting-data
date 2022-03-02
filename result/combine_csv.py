import glob

def read_txt_files() ->list:
    '''
    Function to read csv files created by each thread
    '''
    urls=[]
    txtFiles = glob.glob('*.csv')
    for a in txtFiles:
        file1 = open(a, 'r')
        lines = file1.readlines()
        urls.append(lines)
        file1.close()

    return urls        
  

def write_all_urls_to_txt(urlist:list):
    '''
    Function to write csv files created by each thread
    '''
    file=open('final_properties.csv','w')
    for items in urlist:
        file.writelines(items)

    file.close()

      



a= read_txt_files()
write_all_urls_to_txt(a)