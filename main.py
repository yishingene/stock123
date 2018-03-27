'''
Created on 2018年3月27日
@author: rocky.wang
'''
import fetch_t00_stock_data
import appendRSAK9_t00
import fetch_all_stock_data
import appendRSAK9
def main():

    fetch_t00_stock_data.main()
    
    appendRSAK9_t00.main()
    
    fetch_all_stock_data.main()
    
    appendRSAK9.main()



if __name__ == "__main__":
    main()