import traceback
import lineTool
import os


def main():
    
    a(10, 0)

def a(a, b):
    
    a = [0, 1, 2, 3]
    
    a.insert(1, 5)
    
    print(a)
    
#     return a / b

if __name__ == "__main__":
    try:
        main()
    except:
        msg = traceback.format_exc()
        lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], msg)
        
        
        