# Python program to illustrate the use
# of fast Input / Output
import time, sys
  
# Function to take normal input
def normal_out():
    
      # Stores the start time
    start = time.perf_counter()
  
    # Output Integer
    n = 5
    print(n)
  
    # Output String
    s = "GeeksforGeeks"
    print(s)
  
    # Output List
    arr = [1, 2, 3, 4]
    print(*arr)
  
      # Stores the end time
    end = time.perf_counter()
      
    # Print the time taken
    print("\nTime taken in Normal Output:", \
                      end - start)
  
# Function for Fast Output
def fast_out():
  
    start = time.perf_counter()
    # Output Integer
    n = 5
    sys.stdout.write(str(n)+"\n")
  
    # Output String
    s = "GeeksforGeeks\n"
    sys.stdout.write(s)
  
    # Output Array
    arr = [1, 2, 3, 4]
    sys.stdout.write(
        " ".join(map(str, arr)) + "\n"
    )
          
    # Stores the end time
    end = time.perf_counter()
      
    # Print the time taken
    print("\nTime taken in Fast Output:", \
                      end - start)
  
# Driver Code
if __name__ == "__main__":
  
    # Function Call
    normal_out()
      
    fast_out()