# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
This also doesn't account for if someone is allowed to be alternate for multiple parts

"""

import pandas
import numpy 
import os
import datetime
folder=r"C:\Users\David\OneDrive\Documents\Personal\second_shift\Set List Automation\Data"
file_path=folder+os.path.sep+"Set Lists.xlsx"



def clean_name(name):
    return name.lower().strip()

def clean_role_name(name):
    return name.lower().strip().replace(' ','')
all_person_path=folder+os.path.sep+'all_people.txt'
with open(all_person_path,'r') as file:
    for f in file:
        all_name_set=set([clean_name(name) for name in f.split(', ')])
failed=1
print('ran this')
while failed==1:
    failed=0
    print('while')
    missing_people_str=input("Please provide a list of missing members:")
    # missing_people_str="belen, kristin, ellie"  
    print(missing_people_str)
    print('got here')
    missing_people=[i for i in missing_people_str.split(', ') if len(i)>0]
    
    if len(missing_people)>0:
        for index, person in enumerate(missing_people):
            missing_people[index]=clean_name(person)
            if missing_people[index] not in all_name_set:
                print('Error: "'+person+'" is not a current group member. If this was a typo, please re-type the missing person list. If '+person+' is actually in the group, please add them to the text file here: '+all_person_path )
                failed=1  
       
print('Available group members: '+", ".join(list(all_name_set-set(missing_people))))

song_delete_list=['wings','dance with me tonight']
song_delete_list=[w.lower() for w in song_delete_list]

for index, person in enumerate(missing_people):
    missing_people[index]=clean_name(person)

df=pandas.read_excel(file_path)

var_names = df.columns.values.tolist()

lol=df.values.tolist()

print('got here2')
    
class Song:
    
    def __init__(self,name=""):
        self.name=name
        self.person_dict={}
        self.role_dict={}
        self.alternate_role_dict={}
        self.empty_roles=[]
        self.note_list=[]
        self.eligible_next_songs=[]
        
    def __str__(self):
        print('\n\nsong',self.name)
        for person_name in self.person_dict:
            person=self.person_dict[person_name]
            print(person,person.role_list)
            
        for role_name in self.role_dict:
            role=self.role_dict[role_name]
            print(role)
            for person in role.person_list:
                print(person)
        return 'Song Object: '+self.name
    
    def get_role(self,role_name):
        if role_name in self.role_dict:
            return self.person_dict[self.role_dict[role_name].person_list[0].name]
        else:
            return None
        
    
class Role:
    def __init__(self,name=""):
        self.name=name
        self.person_list=[]
        self.alternate_person_list=[]
        self.missing_person_list=[]
        self.song=None
        self.alternate_role=None
        
        
    def __str__(self):
        return 'Role Object: '+self.name   
    
class Person:
    def __init__(self,name=""):
        self.name=name
        self.role_list=[]
        self.song=None
        
        
        
    def __str__(self):
        
        return 'Person Object: '+self.name   
        

song_list=[]

# =============================================================================
# Recursive function that finds a replacement for a role, a potential replacement for the replacer's role, etc. 
# =============================================================================
def find_replacement(role):
    for person in role.alternate_person_list:
        previous_role_list=person.role_list
        
        if len(previous_role_list)>1:
            for role_temp in previous_role_list:
                if 'solo' not in role_temp.name.lower():
                    raise Exception('Error: multiple previous roles for a replacement person. This should not happen.')                   
        previous_role=previous_role_list[0]
        previous_role_num=len(previous_role.person_list)
        if 'solo' in role.name.lower() and 'solo' in previous_role.name.lower():
            solo=1
        else:
            solo=0
        if previous_role_num>1 or solo:
            return person, previous_role, solo
        else:
            if len(previous_role.alternate_person_list)==0:
                continue
            else:
                replacement_person, previous_previous_role, previous_solo=find_replacement(previous_role)
                if replacement_person is not None:
                    note='Note: replacing '+person.name+' with '+replacement_person.name+' for '+previous_role.name
                    song.note_list.append(note)
                    previous_role.alternate_role.person_list.remove(replacement_person)
                    print(note)
                    
                    if previous_solo==1:
                        
                        replacement_person.role_list.append(previous_role)
                        previous_role.person_list.append(replacement_person)
                    else:
                        replacement_person.role_list=[previous_role]
                        previous_role.person_list.append(replacement_person)
                        previous_previous_role.person_list.remove(replacement_person)
                    return person, previous_role, 0
    return None, None, None
        
        
good_song_names=[]
good_songs=[]
bad_songs=[]   
output_list_good=[]
output_list_bad=[]
output_lookup_good={}
order=0       
print('got here3')

lol=[r for r in lol if r[1].lower() not in song_delete_list]
print(len(lol))
for row in lol:#[3:4]:
# =============================================================================
#     this is the pre-processing to create the initial objects in the right place. 
# =============================================================================
    song=Song(name=row[1])
    song_list.append(song)
    print('got here5')
    print('\n\n',song.name)
    #these have to be separate for loops to avoid creating multiple person objects for a single person
    for i in range(2,len(var_names)):
        role_name=clean_role_name(var_names[i])
        val=row[i]
        if 'alternate' not in role_name:
            if val is not None and isinstance(val,float)==0:
                role=Role(name=role_name)
                role.song=song
                song.role_dict[role_name]=role
                
                for person_name in val.split(', '):
                    person_name=clean_name(person_name)
                    
                    if person_name not in all_name_set:
                        raise Exception('ERROR: "'+person_name+'" is either a typo or not a current group member, but was labeled as a '+role.name+' for '+song.name+'. If this is not correct, please add '+person_name+' to '+all_person_path+'.')
                    if person_name in song.person_dict:
                        raise Exception('ERROR: '+person_name+' appears in both '+role.name+' and '+song.person_dict[person_name].role_list[0].name+' for '+song.name)
                    person=Person(name=person_name)
                    person.song=song
                    person.role_list.append(role)
                    if person_name not in missing_people:
                        
                        song.person_dict[person_name]=person
                        role.person_list.append(person)
                    else:
                        role.missing_person_list.append(person.name)
            else:
                song.empty_roles.append(role_name) 
                
    all_only=all_name_set-set(song.person_dict)-set(missing_people)
    
    if len(all_only)>0:
        raise Exception('ERROR: '+song.name+' did not include at least one group member: '+str(all_only)+'. If these member(s) are not part of the group, please remove them from the current group list at '+all_person_path+'.')
    #these have to be separate for loops to avoid creating multiple person objects for a single person                
    for i in range(2,len(var_names)):  
        role_name=var_names[i].lower().strip().replace(' ','')
        val=row[i]
        if 'alternate' in role_name:
            if val is not None and isinstance(val,float)==0:
                role=Role(name=role_name)
                role.song=song
                song.alternate_role_dict[role_name]=role
                for person_name in val.split(', '):
                    person_name=clean_name(person_name)
                    if person_name not in missing_people:
                        person=song.person_dict[person_name]
                        person.song=song
                        role_name_orig=role_name.replace('alternate','')
                        original_role=song.role_dict[role_name_orig]
                        original_role.alternate_person_list.append(person) 
                        original_role.alternate_role=role
                        role.person_list.append(person)
                    else:
                        role.missing_person_list.append(person.name)
                        
            else:
                song.empty_roles.append(role_name) 
                        

# =============================================================================
#     This part begins the core processing
# =============================================================================
    bad=0

    for role_name in song.role_dict:
        role=song.role_dict[role_name]

        if len(role.person_list)==0:
            replacement_person, previous_role, solo=find_replacement(role)
            if replacement_person is None:
                note='Failed because it could not find a replacement for '+', '.join(role.missing_person_list)+' for '+role.name
                print(note)
                song.note_list.append(note)
                bad=1
            else:
                note='Note: replacing '+', '.join(role.missing_person_list)+' with '+replacement_person.name+' for '+role.name
                role.alternate_role.person_list.remove(replacement_person)
                song.note_list.append(note)
                print(note)
                
                if solo==1:
                    replacement_person.role_list.append(role)
                    role.person_list.append(replacement_person)
                else:
                    replacement_person.role_list=[role]
                    role.person_list.append(replacement_person)
                    previous_role.person_list.remove(replacement_person)
        
    if bad==0:
        order+=1
    row_list=[str(order),song.name]
    
    for var_name in var_names:
        var_name_clean=clean_role_name(var_name)
        if var_name_clean in song.role_dict:
            role_names=", ".join([person.name for person in song.role_dict[var_name_clean].person_list])
            if role_names=="":
                role_names='NO REPLACEMENTS AVAILABLE'
            row_list.append(role_names)

        elif var_name_clean in song.alternate_role_dict:
            role_names=", ".join([person.name for person in song.alternate_role_dict[var_name_clean].person_list])
            if role_names=="":
                role_names='N/A'
            row_list.append(role_names)
        elif var_name_clean in song.empty_roles:
            row_list.append('N/A')
        else:
            if var_name not in ['Order','Song']:
                print('ERROR: there was a variable name that somehow did not end up in the objects')
                print(var_name)
    
    row_list.append(". ".join(song.note_list))
    if bad==1:
        bad_songs.append(song.name)
        output_list_bad.append(row_list)
    else:
        good_song_names.append(song.name)
        good_songs.append(song)
        output_list_good.append(row_list)
        output_lookup_good[song.name]=row_list
        
for song1 in good_songs:
    ineligible_solo_part_list=['solo1','solo2','vp']
    ineligible_solo_list=[song1.get_role(part).name for part in ineligible_solo_part_list if song1.get_role(part) is not None]
    ineligible_vp_part_list=['vp']
    ineligible_vp_list=[song1.get_role(part).name for part in ineligible_vp_part_list if song1.get_role(part) is not None]
    for song2 in good_songs:
        solo_part_list=['solo1','solo2']
        solo_list=[song2.get_role(part).name for part in solo_part_list if song2.get_role(part) is not None]
        vp_part_list=['vp']
        vp_list=[song2.get_role(part).name for part in vp_part_list if song2.get_role(part) is not None]
        problem=False
        for solo in solo_list:
            if solo in ineligible_solo_list:
                problem=True
        
        for vp in vp_list:
            if vp in ineligible_vp_list:
                problem=True
            
        if problem==False:
            song1.eligible_next_songs.append(song2)
            
remaining_song_dict={}
for song in good_songs:
    remaining_song_dict[song.name]=song
def get_next_song(current_song,remaining_song_dict):
    next_song=None
    for possible_song in current_song.eligible_next_songs:
        # if 'tanding' in possible_song.name:
            # print("here!!!",current_song.name,':',possible_song.name)
        if possible_song.name in remaining_song_dict:
            if len(remaining_song_dict)==1:
                # print('lala',possible_song.name)
                return [possible_song,current_song]
            else:
                next_song_dict=remaining_song_dict.copy()
                del next_song_dict[possible_song.name]
                next_return=get_next_song(possible_song,next_song_dict)
                if next_return is None:
                    continue
                else:
                    # print(current_song.name)
                    next_return.append(current_song)
                    # print([s.name for s in next_return])
                    return next_return
            
    if next_song is None:
        return None
   
for song in good_songs:
    next_song_dict=remaining_song_dict.copy()
    del next_song_dict[song.name]
    set_list=get_next_song(song,next_song_dict)

    
    if set_list is not None:
        print('\n\n\nSet List:(',len(set_list),')',set_list)
        break
    
if set_list is None:
    print('Warning: cannot be put in order')
    ordered_output_list=output_list_good
else:
    print('ordering successful!')
    set_list.reverse()
    ordered_output_list=[output_lookup_good[song.name] for song in set_list]

    
    
  
# for song in good_songs:
#     print('\n\n\n',song.name)
#     print([s.name for s in song.eligible_next_songs])
            



        

print()        
        
print('Available Songs (',len(good_song_names),' total):',good_song_names)   
print('Unavailable Songs (',len(bad_songs),' total):',bad_songs)        
for element in ['year','month','day']:
    failed=1
    while failed==1:
        failed=0
        res=input('Please enter the gig '+element+' as a number:')
        if res.isnumeric()==0:
            print('Please enter a number')
            failed=1
        elif '.' in res:
            print('Please do not enter a decimal')
            failed=1
        else:
            try:
                res_int=int(res)
                
            except ValueError:
                print('Please enter an integer')
                failed=1
                continue
            
            if element=='year':
                if res_int<100:
                    print('Note: assuming that this was just the last 2 digits of the year')
                    year=res_int+2000
                elif res_int<2007:
                    print('Please enter a gig date after the group was formed')
                    failed=1
                elif res_int>datetime.datetime.now().year+2:
                    print('Please enter a year that is less than 2 years in the future')
                    failed=1
                else:
                    year=res
            elif element=='month':
                if res_int<1 or res_int>12:
                    print('Please enter a valid month (1-12)')
                    failed=1
                else:
                    month=res
            elif element=='day':
                if res_int<1 or res_int>31:
                    print('please enter a valid day (1-31)')
                    failed=1
                else:
                    day=res
                


gig_name=input('Please enter the gig name:')
    
gig_name="gig_name+'_'+month+'_'+day+'_'+year"
# gig_name="test"
        
var_names.append('Notes')       
df = pandas.DataFrame(ordered_output_list,columns=var_names)
writer = pandas.ExcelWriter(folder+os.path.sep+gig_name+'.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Songs', index=False)
writer.save()
writer.close()
     
df = pandas.DataFrame(output_list_bad,columns=var_names)
writer = pandas.ExcelWriter(folder+os.path.sep+gig_name+'_unavailable_songs.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Songs', index=False)
writer.save()
writer.close()


        

