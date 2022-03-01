import pickle
import glob
def read_txt_files():
    urls=[]
    txtFiles = glob.glob('*.txt')
    for a in txtFiles:
        file1 = open(a, 'r')
        lines = file1.readlines()
        urls.append(lines)
        file1.close()

    return urls        
    #print(txtFiles)

def write_all_urls_to_txt(urlist:list):
    # with open('all_urls.txt', 'w') as fp:
    #     pickle.dump(urlist, fp)

    file=open('combined_urls.txt','w')
    for items in urlist:
        file.writelines(items)

    file.close()


        #fp.write("\n".join(str(item) for item in urlist))



a= read_txt_files()
write_all_urls_to_txt(a)