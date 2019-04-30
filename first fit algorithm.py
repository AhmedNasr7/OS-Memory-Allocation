import sys
import copy
from operator import itemgetter
#segmentsNo
#self.process_Num
#segments_list = []
#hole_list , name to be checked
#memory_size , name to be checked
#########################################

def first_fit(segments_list,hole_list,temp_list,memory_size):


   # temp_list=copy.deepcopy(output_list)#starting address,name,size
    output_list=[]
    temp_hole_list=copy.deepcopy(hole_list)
    segements=0
    temp=0
    hole=0
    i=0


    for n in range (len(segments_list)):
        for k in range (len(temp_hole_list)):
            if(segements_list[n][1]<=temp_hole_list[k][1]):
                    #segement can be put in that hole
                    temp_list.append([temp_hole_list[k][0],segements_list[n][0],segements_list[n][1]])#adding process segement
                    temp_hole_list[k][1]=temp_hole_list[k][1]-segements_list[n][1] #adjusting size in hole list
                    if(temp_hole_list[k][1]==0):
                        temp_hole_list.pop(k)
                    else:
                        temp_hole_list[k][0]=temp_hole_list[k][0]+segements_list[n][1] #adjusting starting address in hole list
                    segements=segements+1
                    break 
###############################################################################################################################################
    if(segements<len(segements_list)): #all segements can 't be allocated
       while(hole<len(hole_list)):
           if(i!=0):
               if(output_list[i-1][0]+output_list[i-1][2]!=hole_list[hole][0]):
                   output_list.append([output_list[i-1][0]+output_list[i-1][2],"Old Process",hole_list[hole][0]-(output_list[i-1][0]+output_list[i-1][2])])
                   i=i+1
           output_list.append([hole_list[hole][0],"HOLE",hole_list[hole][1]])
           hole=hole+1
           i=i+1

       n=len(output_list)
       if(output_list[n-1][0]+output_list[n-1][2]!=memory_size):
           starting_address=output_list[n-1][0]+output_list[n-1][2]
           size=memory_size-starting_address
           output_list.append([starting_address,"Old Process",size])
       return output_list,hole_list,temp_list


   ############################################################################################################################################
    else:#merge
       temp_list=sorted(temp_list,key=itemgetter(0))
       hole_list=temp_hole_list
       while(temp<len(temp_list)and hole<len(temp_hole_list)):
           ###########temp will be put in output##############################################
           if(temp_list[temp][0]<temp_hole_list[hole][0]):

            if(i!=0):
             if(output_list[i-1][0]+output_list[i-1][2]!=temp_list[temp][0]):
                 output_list.append([output_list[i-1][0]+output_list[i-1][2],"Old Process",temp_list[temp][0]-(output_list[i-1][0]+output_list[i-1][2])])
                 i=i+1

            output_list.append([temp_list[temp][0],temp_list[temp][1],temp_list[temp][2]])
            temp=temp+1
            i=i+1
            
             

       ####hole will be put in output###########################################        
           else:
               if(i!=0):
                if(output_list[i-1][0]+output_list[i-1][2]!=temp_hole_list[hole][0]):
                  output_list.append([output_list[i-1][0]+output_list[i-1][2],"Old Process",temp_hole_list[hole][0]-(output_list[i-1][0]+output_list[i-1][2])])
                  i=i+1
               output_list.append([temp_hole_list[hole][0],"HOLE",temp_hole_list[hole][1]])
               hole=hole+1
               i=i+1
                
#####what's left off from any of the two lists##################################       
       while(temp<len(temp_list)):
           if(i!=0):
                if(output_list[i-1][0]+output_list[i-1][2]!=temp_list[temp][0]):
                  output_list.append([output_list[i-1][0]+output_list[i-1][2],"Old Process",temp_list[temp][0]-(output_list[i-1][0]+output_list[i-1][2])])
                  i=i+1
           output_list.append([temp_list[temp][0],temp_list[temp][1],temp_list[temp][2]])
           temp=temp+1
           i=i+1
       while(hole<len(temp_hole_list)):
            if(i!=0):
                if(output_list[i-1][0]+output_list[i-1][2]!=temp_hole_list[hole][0]):
                  output_list.append([output_list[i-1][0]+output_list[i-1][2],"Old Process",temp_hole_list[hole][0]-(output_list[i-1][0]+output_list[i-1][2])])
                  i=i+1
            output_list.append([temp_hole_list[hole][0],"HOLE",temp_hole_list[hole][1]])
            hole=hole+1
            i=i+1
       n=len(output_list)
       if(output_list[n-1][0]+output_list[n-1][2]!=memory_size):
           starting_address=output_list[n-1][0]+output_list[n-1][2]
           size=memory_size-starting_address
           output_list.append([starting_address,"Old Process",size])
       return output_list,hole_list,temp_list    
            
##       
##              
###test cases          
##print("1st test case")   #multiple segements         
##hole_list=[[0,80],[90,200]]
##temp_list=[]
##segements_list=[['code',20],['stack',50],['local',100]]
##output_list,hole_list,new_segements=first_fit(segements_list,hole_list,temp_list,290)
##print(output_list)
##
##print("another segement")
##segements_list=[['code2',10],['stack2',50]]
##output_list,hole_list,new_segements=first_fit(segements_list,hole_list,new_segements,290)
##print(output_list)
##
##print("2nd test case")#not enough space
##hole_list=[[0,50],[60,30]]
##temp_list=[]
##segements_list=[['code',20],['stack',50],['local',100]]
##output_list,hole_list,new_segements=first_fit(segements_list,hole_list,temp_list,90)
##print(output_list)
##
##
##
##print("3rd test case")#reversed oder of segement size
##hole_list=[[0,50],[60,30],[100,200]]
##segements_list=[['code',100],['stack',30]]
##temp_list=[]
##output_list,hole_list,new_segements=first_fit(segements_list,hole_list,temp_list,300)
##print(output_list)
##
##print("4th test case")#reversed order + multiple segements
##hole_list=[[0,80],[90,200]]
##temp_list=[]
##segements_list=[['code',20],['stack',50],['local',100]]
##output_list,hole_list,new_segements=first_fit(segements_list,hole_list,temp_list,290)
##print(output_list)
##
##print("another segement")
##segements_list=[['code2',50],['stack2',10]]
##output_list,hole_list,new_segements=first_fit(segements_list,hole_list,new_segements,290)
##print(output_list)
##
##
##print("5th test case") #extra space in memory at the end+ not enough space
##hole_list=[[0,50],[60,30]]
##temp_list=[]
##segements_list=[['code',20],['stack',50],['local',100]]
##output_list,hole_list,new_segements=first_fit(segements_list,hole_list,temp_list,100)
##print(output_list)
##
##print("6th test case")
##hole_list=[[0,80],[90,200]]
##temp_list=[]
##segements_list=[['code',20],['stack',50],['local',100]]
##output_list,hole_list,new_segements=first_fit(segements_list,hole_list,temp_list,300)
##print(output_list)
##
##print("another segement")
##segements_list=[['code2',10],['stack2',50]]
##output_list,hole_list,new_segements=first_fit(segements_list,hole_list,new_segements,300)
##print(output_list)

                    
