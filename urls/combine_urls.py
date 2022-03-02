import glob
def read_txt_files()->list:
    '''
    Function to combine txt files created by each thread
    '''
    urls=[]
    txtFiles = glob.glob('*.txt')
    for a in txtFiles:
        file1 = open(a, 'r')
        lines = file1.readlines()
        urls.append(lines)
        file1.close()

    return urls        
   

def write_all_urls_to_txt(urlist:list):
    '''
    Function to write txt files created by each thread
    '''

    file=open('combined_urls.txt','w')
    for items in urlist:
        file.writelines(items)

    file.close()





a= read_txt_files()
write_all_urls_to_txt(a)