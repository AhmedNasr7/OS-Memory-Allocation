import hashlib 
import copy
from operator import itemgetter

class Memory():

    def __init__(self, memory_size):
        
        self.memory_contents = [["default", self.color_from_name("default"), memory_size]]
        self.memory_size = memory_size

        
    def color_from_name(self, process_name="hole"):
        return hashlib.md5(process_name.encode()).hexdigest()[0:6]

    def first_fit(self, segments_list , hole_list ,memory_size):

        # starting address,name,size
        temp2_list=[]
        output_list=[]
        temp_list=[]
        temp=0
        hole=0
        hole_number=0
        i=0


        for n in range (len(segments_list)):
            temp_hole_list=copy.deepcopy(hole_list)
            segements=0
            for j in range (len(segements_list[n])):

             for k in range (len(temp_hole_list)):

                if(segements_list[n][j][1]<=temp_hole_list[k][1]):

                        #segement can be put in that hole
                        
                        temp_list.append([temp_hole_list[k][0],"P"+str(n)+":"+segements_list[n][j][0],segements_list[n][j][1]])#adding process segement
                        temp_hole_list[k][1]=temp_hole_list[k][1]-segements_list[n][j][1] #adjusting size in hole list

                        if(temp_hole_list[k][1]==0):
                            temp_hole_list.pop(k)
                        else:
                            temp_hole_list[k][0]=temp_hole_list[k][0]+segements_list[n][j][1] #adjusting starting address in hole list
                        segements=segements+1
                        break 
       
            if(segements==len(segements_list[n])):
                hole_list=copy.deepcopy(temp_hole_list)
                temp2_list=copy.deepcopy(temp_list)
        

    ######################MERGE########################################################################################
       
        temp2_list=sorted(temp2_list,key=itemgetter(0))
        while(temp<len(temp2_list)and hole<len(hole_list)):
               
               ###########temp will be put in output##############################################
               if(temp2_list[temp][0]<hole_list[hole][0]):

                if(i!=0):
                 if(output_list[i-1][0]+output_list[i-1][2]!=temp2_list[temp][0]):
                     output_list.append([output_list[i-1][0]+output_list[i-1][2],"Old Process",temp2_list[temp][0]-(output_list[i-1][0]+output_list[i-1][2])])
                     i=i+1

                output_list.append([temp2_list[temp][0],temp2_list[temp][1],temp2_list[temp][2]])
                temp=temp+1
                i=i+1
                
                 

           ####hole will be put in output###########################################        
               else:
                   if(i!=0):
                    if(output_list[i-1][0]+output_list[i-1][2]!=hole_list[hole][0]):
                      output_list.append([output_list[i-1][0]+output_list[i-1][2],"Old Process",hole_list[hole][0]-(output_list[i-1][0]+output_list[i-1][2])])
                      i=i+1
                   output_list.append([hole_list[hole][0],"HOLE"+str(hole_number),hole_list[hole][1]])
                   hole_number=hole_number+1
                   hole=hole+1
                   i=i+1
                    
    #####what's left off from any of the two lists##################################       
        while(temp<len(temp2_list)):
               if(i!=0):
                    if(output_list[i-1][0]+output_list[i-1][2]!=temp2_list[temp][0]):
                      output_list.append([output_list[i-1][0]+output_list[i-1][2],"Old Process",temp_list[temp][0]-(output_list[i-1][0]+output_list[i-1][2])])
                      i=i+1
               output_list.append([temp2_list[temp][0],temp2_list[temp][1],temp2_list[temp][2]])
               temp=temp+1
               i=i+1
        while(hole<len(hole_list)):
                if(i!=0):
                    if(output_list[i-1][0]+output_list[i-1][2]!=hole_list[hole][0]):
                      output_list.append([output_list[i-1][0]+output_list[i-1][2],"Old Process",hole_list[hole][0]-(output_list[i-1][0]+output_list[i-1][2])])
                      i=i+1
                output_list.append([hole_list[hole][0],"HOLE"+str(hole_number),hole_list[hole][1]])
                hole_number=hole_number+1
                hole=hole+1
                i=i+1
        n=len(output_list)
        if(output_list[n-1][0]+output_list[n-1][2]!=memory_size):
               starting_address=output_list[n-1][0]+output_list[n-1][2]
               size=memory_size-starting_address
               output_list.append([starting_address,"Old Process",size])
        self.memory_contents=copy.deepycopy(output_list)
        return self.memory_contents



    def best_fit(self):
        pass

    def worst_fit(self, Memory, Segments, process_name="default"):
        
        color = self.color_from_name(process_name)
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

    def compact(self):
        pass
    
    def add_hole(self, starting_address, hole_size):
        assert(starting_address + hole_size <= self.memory_size)
        sum = 0
        for i in range(len(self.memory_contents)):
            sum = sum + self.memory_contents[i][2]
            if(sum > starting_address):
                assert(self.memory_contents[i][0] == "default")
                assert(sum - (starting_address + hole_size) >= 0)
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
                    
        # self.memory_contents.insert[]
    
    def deallocate(self, process_name):
        pass


    def get_memoryContents(self):
        '''
        a function that retutrns the list of memory processes/segments
        '''    
        return self.memory_contents


Segments = [["Code", 5],
            ["Data", 90],
            ["Stack", 15]]

memory = Memory(5000)
memory.add_hole(2000, 3000)
print(memory.get_memoryContents())
# Memory, _ = worst_fit(Memory, Segments, "p1")
# print(Memory, _)
