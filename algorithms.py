# Implementation of OS algorithms
 
import hashlib 

def color_from_name(process_name="hole"):
    return hashlib.md5(process_name.encode()).hexdigest()[0:6]

def first_fit():
    pass


def best_fit():
    pass

def worst_fit(Memory, Segments, process_name="default"):
    
    color = color_from_name(process_name)
    error = 0

    for segment in Segments:
        Max = 0
        for i in range(len(Memory)):
            if(Memory[i][2] > Memory[Max][2] and Memory[i][0] == "hole"):
                Max = i
        
        if(Memory[Max][2] < segment[1]):
            error = 1
            return Memory, error

        Memory.insert(Max, [segment[0], color, segment[1]])

        if(Memory[Max+1][2] == segment[1]):
            Memory.pop(Max+1)
        else:
            Memory[Max+1][2] = Memory[Max+1][2] - segment[1]
        
    
    return Memory, error


def compact():
    pass


Memory = [["hole", "ca3143", 100]]
Segments = [["Code", 5],
            ["Data", 90],
            ["Stack", 15]]

Memory, _ = worst_fit(Memory, Segments, "p1")
print(Memory, _)