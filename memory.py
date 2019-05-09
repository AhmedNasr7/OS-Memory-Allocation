import hashlib 
import copy
from operator import itemgetter

class Memory():

    def __init__(self, memory_size):
        
        self.memory_contents = [["default", self.color_from_name("default"), memory_size]]
        self.memory_size = memory_size

    @staticmethod
    def color_from_name(process_name="hole"):
        return hashlib.md5(process_name.encode()).hexdigest()[0:6]

    def first_fit(self, segments_list, process_name):
        #name,color,size
        output_list=copy.deepcopy(self.memory_contents)
        color=self.color_from_name(process_name)                                                                                                                                                                                                                                                                                                                                                                                            
        segements=0
        
        for i in range (len(segments_list)):
            for j in range (len(output_list)):
                if(output_list[j][0]=='hole'):
                    if(output_list[j][2]>=segments_list[i][1]):
                       output_list[j][2]= output_list[j][2]-segments_list[i][1]
                       output_list.insert(j,[segments_list[i][0],color,segments_list[i][1]])
                       if(output_list[j+1][2]==0):
                           output_list.pop(j+1)
                       segements=segements+1
                       break            
       
            if(segements==len(segments_list)):
             self.memory_contents=copy.deepcopy(output_list)
      
    def best_fit(self, segments, process_name):
        min_size = self.memory_size + 1 
        hole_index = 0

        for segment in segments:
            segment_size = segment[1]
            for i in range(self.memory_contents):
                hole = self.memory_contents[i]
                if (hole[0] == 'hole'):
                    hole_size = hole[2]
                    if ((hole_size >= segment_size) and (hole_size < min_size)):
                        min_size = hole_size
                        hole_index = i
            
            best_hole = self.memory_contents[hole_index]
            hole_size = best_hole[2]
            left_over = segment_size - hole_size
            if(left_over > 0):
                best_hole[2] = left_over
                self.memory_contents[hole_index] = best_hole
                self.memory_contents.insert(hole_index, [process_name, self.color_from_name(process_name), segment_size])
            else:
                self.memory_contents[hole_index] = [process_name, self.color_from_name(process_name), segment_size]

    def worst_fit(self, Segments, process_name="default"):      
        color = self.color_from_name(process_name)

        for segment in Segments:
            Max = 0
            for i in range(len(self.memory_contents)):
                if(self.memory_contents[i][2] > self.memory_contents[Max][2] and self.memory_contents[i][0] == "hole"):
                    Max = i
        
            assert(self.memory_contents[Max][2] >= segment[1]), "Memory limit Excedded"

            self.memory_contents.insert(Max, [segment[0], color, segment[1]])

            if(self.memory_contents[Max+1][2] == segment[1]):
                self.memory_contents.pop(Max+1)
            else:
                self.memory_contents[Max+1][2] = self.memory_contents[Max+1][2] - segment[1]


    def compact(self):
        holes_sum = 0
        for hole in self.memory_contents[:]:
            if(hole[0] == "hole"):
                holes_sum = holes_sum + hole[2]
                self.memory_contents.remove(hole)
        
        self.memory_contents.insert(0, ["hole", self.color_from_name(), holes_sum])
        
        
    def Merge(self):
        Flag = 1
        while(Flag):
            Flag = 0
            for i in range(len(self.memory_contents) - 1):
                if(self.memory_contents[i][0] == self.memory_contents[i+1][0]):
                    self.memory_contents[i][2] = self.memory_contents[i][2] + self.memory_contents[i+1][2]
                    self.memory_contents.pop(i+1)
                    Flag = 1
                    break
                
    
    def add_hole(self, starting_address, hole_size):
        assert starting_address + hole_size <= self.memory_size, "Hole Address or Size exceeds memory limits, please reassign their values"
        sum = 0
        for i in range(len(self.memory_contents)):
            sum = sum + self.memory_contents[i][2]
            if(sum > starting_address):
                assert(self.memory_contents[i][0] == "default"), "Can't add a hole here"
                assert(sum - (starting_address + hole_size) >= 0), "Hole size excedded the limits"
                if sum - (starting_address + hole_size) == 0:
                    self.memory_contents[i][2] -= hole_size
                    self.memory_contents.insert(i+1, ["hole", self.color_from_name("hole"), hole_size])
                    break
                else:
                    self.memory_contents[i][2] = self.memory_contents[i][2] - (sum - starting_address)
                    self.memory_contents.insert(i+1, ["hole", self.color_from_name("hole"), hole_size])
                    self.memory_contents.insert(i+2, ["default", self.color_from_name("default"), sum - (starting_address + hole_size)])
                    if (self.memory_contents[i][2] == 0):
                        self.memory_contents.pop(i)
                    break
                    
    
    def deallocate(self, process_name):
        color = self.color_from_name(process_name)
        for i in range(len(self.memory_contents)):
            if(self.memory_contents[i][1] == color):
                self.memory_contents[i] = ["hole", self.color_from_name(), self.memory_contents[i][2]]


    def get_memoryContents(self):
        '''
        return list of memory processes/segments
        '''    
        return self.memory_contents

def main():
    # # Testing
    Segments = [["Code", 50],
                ["Data", 90],
            ["Stack", 15]]

    memory = Memory(5000)

    memory.add_hole(2000, 500)

    memory.add_hole(0,700)

    memory.add_hole(1000, 1000)

    memory.add_hole(3000, 800)

    print(memory.get_memoryContents())
    # memory.compact()
    # print(memory.get_memoryContents())
    memory.Merge()
    print(memory.get_memoryContents())
    # memory.worst_fit(Segments, "P1")
    # print(memory.get_memoryContents())
    # memory.deallocate("P1")
    # print(memory.get_memoryContents())
    # memory.compact()
    # print(memory.get_memoryContents())
    # memory.Merge()
    # print(memory.get_memoryContents())

if __name__ == "__main__":
    main()