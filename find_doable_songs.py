# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
This also doesn't account for if someone is allowed to be alternate for multiple parts

"""



"""--------------------------------------------------"""
"""AMITHA SECTION 1 START"""
"""--------------------------------------------------"""
import math
import pandas
import os
import datetime
from datetime import date

# =============================================================================
# Get list of manually eliminated orderings
# =============================================================================

today = date.today()


"https://docs.google.com/spreadsheets/d/1z1c632UCyPgrChQjbOFAwJdHVgKyJd1oi2c7-TGCJt0/edit?usp=sharing"

SHEET_ID = '1z1c632UCyPgrChQjbOFAwJdHVgKyJd1oi2c7-TGCJt0'
SHEET_NAME_Songs = 'Songs'
SHEET_NAME_Members = 'Members'
SHEET_NAME_Orderings = 'Banned_Orderings'
url_Songs = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME_Songs}'
url_Members = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME_Members}'
url_Orderings = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME_Orderings}'


df_set_list = pandas.read_csv(url_Songs)
df_members = pandas.read_csv(url_Members)
df_banned_orderings = pandas.read_csv(url_Orderings)



# df_set_list=pandas.read_excel("Set Lists.xlsx")
# df_members = pandas.read_excel("Set Lists.xlsx", sheet_name="Members")
# df_banned_orderings = pandas.read_excel("Set Lists.xlsx", sheet_name="Banned Orderings")






songs = df_set_list["Song"].values.tolist()
song_delete_list = []
ban_lookup={}
for index, row in df_banned_orderings.iterrows():
    song1=row['Song1'].lower()
    song2=row['Song2'].lower()
    if song1 in ban_lookup:
        ban_lookup[song1].append(song2)
    else:
        ban_lookup[song1]=[song2]
        
list_all_names = df_members["Names"].values.tolist()
members = sorted(list_all_names)
gui_missing_people = []
global Notes_list
    
def program_run():
    timenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S%z")[0:13] + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S%z")[14:16] + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S%z")[17:19]
    run_label.config(text = "Running...")
    
    Notes_list = []
    
    
    gig_name = gig_entry.get() # Retrieve gig name
    gig_date = str(cal.selection_get()) # Retrieve gig date as string
    missing_people_str = ", ".join(gui_missing_people) # Retrieve missing people as comma-separated string
    num_songs_needed = int(number_of_songs.get()) # Retrieve total # of songs
    num_breaks_needed = int(set_break.get()) # Retrieve # of breaks
    
    set_length = math.ceil(num_songs_needed / (num_breaks_needed+1))  # Calculate largest set length
    remainder = num_songs_needed % (num_breaks_needed+1)  # Check if set lengths are all equal
    tracker = remainder # Create tracker variable for varying set lengths
    
    break_list = []
    current_position = set_length  # Start from the largest set length
    
    for i in range(num_breaks_needed):
        if remainder > 0: # only if set lenghts are not equal
            tracker -= 1 # update the tracker
            if tracker < 0: # if threshold reached
                current_position -= 1  # Reduce set length by 1 
        break_list.append(current_position)  # Add the break position to the list
        current_position += set_length  # Move to the next set length
    """--------------------------------------------------"""
    """AMITHA SECTION 1 END"""
    """--------------------------------------------------"""
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    import random    
    
    def clean_name(name):
        return name.lower().strip()
    
    def clean_role_name(name):
        return name.lower().strip().replace(' ','')

    all_name_set=set([w.lower() for w in members])

    missing_people=[i for i in missing_people_str.split(', ') if len(i)>0]

    
    
    break_list=[b+1 for b in break_list]
    
    
    for index, person in enumerate(missing_people):
        missing_people[index]=clean_name(person)
    
    var_names = df_set_list.columns.values.tolist()
    
    lol=df_set_list.values.tolist()
        
    class Song:
        
        def __init__(self,name="",song_type="Standard"):
            self.name=name
            self.person_dict={}
            self.role_dict={}
            self.alternate_role_dict={}
            self.empty_roles=[]
            self.note_list=[]
            self.eligible_next_songs=[]
            self.eligible_next_sa_tb=[]
            self.song_type=song_type
            self.num_replacements=0
            self.can_precede_break=False
            #to keep track of whether the sa/tb songs have been used
            self.used='unknown'
            
        def __str__(self):
            return 'Song Object: '+self.name
        
        def get_role(self,role_name):
            if role_name in self.role_dict:
                return self.person_dict[self.role_dict[role_name].person_list[0].name]
            else:
                return None
            
    def remove_element(lst, element):
        return [x for x in lst if x != element]    
    
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
        
        def remove_alternate(self,person):
            self.alternate_person_list=remove_element(self.alternate_person_list,person)
            self.alternate_role.person_list=remove_element(self.alternate_role.person_list,person)
            person.role_list=remove_element(person.role_list,self.alternate_role)
        
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
                        Notes_list.append('\nError: multiple previous roles for a replacement person. This should not happen.')
            previous_role=previous_role_list[0]
            previous_role_num=len(previous_role.person_list)
            if 'solo' in role.name.lower() and 'solo' in previous_role.name.lower():
                solo=1
            else:
                solo=0
            if previous_role_num>1 or solo:
                role.remove_alternate(person)
                return person, previous_role, solo
            else:
                if len(previous_role.alternate_person_list)==0:
                    continue
                else:
                    replacement_person, previous_previous_role, previous_solo=find_replacement(previous_role)
                    
                    if replacement_person is not None:
                        note="\n" + song.name + 'Note: replacing '+person.name+' with '+replacement_person.name+' for '+previous_role.name
                        song.num_replacements+=1
                        song.note_list.append(note)
                        Notes_list.append(note)
                        
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
    sa_tb_songs=[]
    output_lookup_good={}
    order=0       
    
    lol=[r for r in lol if isinstance(r[1],str) and r[1].lower() not in song_delete_list]
    
    num_retired_songs=len([r for r in lol if r[2].lower()=='retired'])
    for row in lol:#[3:4]:
    # =============================================================================
    #     this is the pre-processing to create the initial objects in the right place. 
    # =============================================================================
        song=Song(name=row[1],song_type=row[2])
        song_list.append(song)
        #these have to be separate for loops to avoid creating multiple person objects for a single person
        start_row_index=3
        for i in range(start_row_index,len(var_names)):
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
                            raise Exception('ERROR: "'+person_name+'" is either a typo or not a current group member, but was labeled as a '+role.name+' for '+song.name+'. If this is not correct, please add '+person_name+' to the Members tab of the spreadsheet.')
                            Notes_list.append('\nERROR: "'+person_name+'" is either a typo or not a current group member, but was labeled as a '+role.name+' for '+song.name+'. If this is not correct, please add '+person_name+' to the Members tab of the spreadsheet.')
                        if person_name in song.person_dict:
                            raise Exception('ERROR: '+person_name+' appears in both '+role.name+' and '+song.person_dict[person_name].role_list[0].name+' for '+song.name)
                            Notes_list.append('\nERROR: '+person_name+' appears in both '+role.name+' and '+song.person_dict[person_name].role_list[0].name+' for '+song.name)
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
            raise Exception('ERROR: '+song.name+' did not include at least one group member: '+str(all_only)+'. If these member(s) are not part of the group, please remove them from the Members tab of the spreadsheet.')
            Notes_list.append('\nERROR: '+song.name+' did not include at least one group member: '+str(all_only)+'. If these member(s) are not part of the group, please remove them from the Members tab of the spreadsheet.')
        #these have to be separate for loops to avoid creating multiple person objects for a single person                
        for i in range(start_row_index,len(var_names)):  
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
                    note=song.name +' failed because it could not find a replacement for '+', '.join(role.missing_person_list)+' for '+role.name
                    Notes_list.append("\n"+note)
                    song.note_list.append(note)
                    bad=1
                else:
                    note=song.name + ' note: replacing '+', '.join(role.missing_person_list)+' with '+replacement_person.name+' for '+role.name
                    Notes_list.append("\n"+note)
                    song.note_list.append(note)
                    
                    if solo==1:
                        replacement_person.role_list.append(role)
                        role.person_list.append(replacement_person)
                    else:
                        replacement_person.role_list=[role]
                        role.person_list.append(replacement_person)
                        previous_role.person_list.remove(replacement_person)
            
        if bad==0:
            order+=1
        row_list=[str(order),song.name,song.song_type]
        
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
                if var_name not in ['Order','Song','Type']:
                    Notes_list.append('\nERROR: there was a variable name ' + var_name + ' that somehow did not end up in the objects')
        
        row_list.append(". ".join(song.note_list))
        if bad==1:
            bad_songs.append("\n"+song.name)
            output_list_bad.append(row_list)
        else:
            good_song_names.append("\n"+song.name)
            if song.song_type in ['tb','sa']:
                sa_tb_songs.append(song)
            else:
                good_songs.append(song)
            output_list_good.append(row_list)
            output_lookup_good[song.name]=row_list
                
    
    # =============================================================================
    # this part gets a list of eligible next songs for each song
    # =============================================================================
    for song1 in good_songs:
        ineligible_solo_part_list=['solo1','solo2','vp']
        ineligible_solo_list=[song1.get_role(part).name for part in ineligible_solo_part_list if song1.get_role(part) is not None]
        ineligible_vp_part_list=['vp']
        ineligible_vp_list=[song1.get_role(part).name for part in ineligible_vp_part_list if song1.get_role(part) is not None]
        for song2 in good_songs+sa_tb_songs:
            solo_part_list=['solo1','solo2']
            solo_list=[song2.get_role(part).name for part in solo_part_list if song2.get_role(part) is not None]
            vp_part_list=['vp']
            vp_list=[song2.get_role(part).name for part in vp_part_list if song2.get_role(part) is not None]
            problem=False
            #checks to see if a combination has is on the manual banned_orderings list
            if song1.name.lower() in ban_lookup:
                if song2.name.lower() in ban_lookup[song1.name.lower()]:
                    problem=True
            for solo in solo_list:
                if solo in ineligible_solo_list:
                    problem=True
            
            for vp in vp_list:
                if vp in ineligible_vp_list:
                    problem=True
                
            if problem==False:
                if song2.song_type=='tb':
                    song1.can_precede_break=True
                elif song2.song_type!='sa':
                    song1.eligible_next_songs.append(song2)
                
    remaining_song_dict={}
    for song in good_songs:
        remaining_song_dict[song.name]=song
        
    # =============================================================================
    #     This is used to recursively search for set list orderings that work
    # =============================================================================
    def get_next_song(current_song,remaining_song_dict,num_leftover_songs=None, song_count=None, break_list=None, good_songs=None, sa_tb_songs=None, retired_songs=0):
        if current_song.song_type=='retired':
            retired_songs+=-1
        if retired_songs<0:
            return None
        
        first_sa_tb=False
        if song_count+1 not in break_list:
            eligible_next_songs=current_song.eligible_next_songs
            
        else:
            eligible_next_songs=good_songs
            if len(sa_tb_songs)>=2 and sa_tb_songs[0].used != True:
                first_sa_tb=True
                num_leftover_songs+=2
                for song_temp in sa_tb_songs:
                    song_temp.used=True
        if retired_songs==0:
            eligible_next_songs=[e for e in eligible_next_songs if e.song_type.lower() != 'retired']   
    
        eligible_next_songs_sort=[]
        for song in eligible_next_songs:
            eligible_next_songs_sort.append([song,song.song_type+'_'+str(song.num_replacements)+'_'+str(random.uniform(0,1))])
    
        eligible_next_songs_sort.sort(key = lambda x: x[1])
        for possible_song in eligible_next_songs_sort:

            
            possible_song=possible_song[0]
            if possible_song.name in remaining_song_dict:
                temp_diff=len(remaining_song_dict)-1-num_leftover_songs
                if temp_diff<=0:
                    if temp_diff==0:
                        next_return=[possible_song,current_song]
                    else:
                        next_return=[current_song]
                    if first_sa_tb==True:
                        next_return+=sa_tb_songs
                        
                    return next_return
                else:
                    next_song_dict=remaining_song_dict.copy()
                    del next_song_dict[possible_song.name]
    
                    next_return=get_next_song(possible_song,next_song_dict,num_leftover_songs=num_leftover_songs, song_count=song_count+1, break_list=break_list, good_songs=good_songs, sa_tb_songs=sa_tb_songs, retired_songs=retired_songs)
                    if next_return is None:
                        continue
                    else:
                        next_return.append(current_song)
                        if first_sa_tb==True:
                            next_return+=sa_tb_songs
                            
                            
                        return next_return
    
        return None
    # =============================================================================
    # Recursively find a set list ordering that works, if possible
    # =============================================================================
    if len(good_songs)>=num_songs_needed:  
        num_leftover_songs=len(good_songs)-num_songs_needed
        for song in good_songs:
            next_song_dict=remaining_song_dict.copy()
            del next_song_dict[song.name]
            set_list=None
            for i in range(num_retired_songs+1):
                if set_list is None:
                    set_list=get_next_song(song,next_song_dict,num_leftover_songs=num_leftover_songs,song_count=1, break_list=break_list, good_songs=good_songs, sa_tb_songs=sa_tb_songs, retired_songs=i)
                    if set_list is not None:
                        break
                    
            if i>0 and set_list is not None:
                Notes_list.append('\n\nWarning: used '+str(i)+' retired song(s)!')
        
            
            if set_list is not None:
                break
        if set_list is None:
            Notes_list.append('\nWarning: songs cannot be put in order')
    else:
        set_list=None
        Notes_list.append('\nWarning: not enough valid songs to make the desired set list')
        
    if set_list is None:
        ordered_output_list=output_list_good
        run_label.config(text = 'ordering failed')
    else:
        run_label.config(text = 'ordering successful!')
        set_list.reverse()
        ordered_output_list=[]
        index=1
        song_index=1
        for song in set_list:
            row=output_lookup_good[song.name]
            row[0]=index
            ordered_output_list.append(row)
            index+=1
            song_index+=1
            if song_index in break_list and (len(sa_tb_songs)<2 or song_index>break_list[0]):
                break_row=[]
                for element in row:
                    break_row.append('---')
                break_row[1]='[break]'
                break_row[0]=index
                ordered_output_list.append(break_row)
                index+=1
                
    
    
    # =============================================================================
    # Add back in the songs that aren't in the ordered set list, but could be used
    # =============================================================================
    if len(good_songs)>num_songs_needed:
        
        used_set=set()
        break_row=[]
        for element in ordered_output_list[0]:
            break_row.append('---')
        break_row[1]='[end of set]'
        break_row[0]=index
        ordered_output_list.append(break_row)
        index+=1
        for song in ordered_output_list:
            used_set.add(song[1])
            
        for song in output_list_good:
            if song[1] not in used_set:
                song[0]=index
                ordered_output_list.append(song)
                index+=1
    
                
    
    label_songs_available.config(justify="left", text = 'Available Songs ('+ str(len(good_song_names))+' total):'+ ''.join(good_song_names))
    label_notes.config(justify="left", text = ''.join(Notes_list))
    label_songs_unavailable.config(justify="left", text = '\nUnavailable Songs ('+str(len(bad_songs))+' total):'+''.join(bad_songs))
    
    
    
    var_names.append('Notes')      
    
    df = pandas.DataFrame(ordered_output_list,columns=var_names)
    output_folder=os.getcwd()+os.path.sep+gig_name + " " + timenow
    if os.path.exists(output_folder)==0:
        os.makedirs(output_folder)
    writer = pandas.ExcelWriter(output_folder+os.path.sep+gig_name+gig_date+ " " + timenow+'.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Songs', index=False)
    df.to_csv(output_folder+os.path.sep+gig_name+'.txt', index=False, sep='\t')
    writer.save()
    # writer.close()
         
    df = pandas.DataFrame(output_list_bad,columns=var_names)
    writer = pandas.ExcelWriter(output_folder+os.path.sep+gig_name+gig_date+'_unavailable_songs.xlsx', engine='xlsxwriter')
    df.to_csv(output_folder+os.path.sep+gig_name+'_unavailable_songs.txt', index=False, sep='\t')
    df.to_excel(writer, sheet_name='Songs', index=False)
    writer.save()
    # writer.close()
    
    
        





































"""--------------------------------------------------"""
"""AMITHA SECTION 2 START"""
"""--------------------------------------------------"""
from tkcalendar import Calendar

try:
    import tkinter as tk
    from tkinter import Checkbutton, IntVar
except ImportError:
    import Tkinter as tk
from functools import partial
global event_date


def remove(index, songs):
    if var_list_songs[index].get() == 1:
        song_delete_list.append(songs[index].lower())
    if (var_list_songs[index].get() == 0) & (songs[index].lower() in (song_delete_list)):
        song_delete_list.remove(songs[index].lower())

def absent(index, members):
    if var_list_members[index].get() == 1:
        gui_missing_people.append(members[index].lower())
    if (var_list_members[index].get() == 0) & (members[index].lower() in (gui_missing_people)):
        gui_missing_people.remove(members[index].lower())
    


window = tk.Tk()

frame_gig_specs = tk.Frame()
tk.Label(frame_gig_specs, text="Enter Gig Name").grid(row=0,column=0)
tk.Label(frame_gig_specs, text="(no special characters)").grid(row=1,column=0)
gig_entry = tk.Entry(frame_gig_specs, width = 30)
gig_entry.insert(-1, "SAMPLE")
gig_entry.grid(row=2,column=0, pady=(0, 0))

tk.Label(frame_gig_specs, text="Select # of songs").grid(row=3,column=0, pady=(20, 0))
number_of_songs = tk.StringVar(frame_gig_specs)
set_lengths = list(range(1,21))
number_of_songs.set(set_lengths[0]) # default value
number_of_songs_ = tk.OptionMenu(frame_gig_specs, number_of_songs, *set_lengths)
number_of_songs_.grid(row=4,column=0)

tk.Label(frame_gig_specs, text="Select # of breaks").grid(row=5,column=0, pady=(20, 0))
set_break = tk.StringVar(frame_gig_specs)
set_breaks = [0, 1, 2, 3]
set_break.set(set_breaks[0]) # default value
set_break_ = tk.OptionMenu(frame_gig_specs, set_break, *set_breaks)
set_break_.grid(row=6,column=0)



frame_gig_date = tk.Frame()
label_b = tk.Label(frame_gig_date, text='Select Event Date').pack()
cal = Calendar(frame_gig_date, font="Arial 10", selectmode='day',cursor="hand1", 
               year=today.year, month=today.month, day=today.day)
cal.pack(fill="both", pady=0)



frame_missing = tk.Frame()
tk.Label(frame_missing, text="Select Absent Members").pack(anchor="nw")

var_list_members = []
for index, member in enumerate(members):
    var_list_members.append(IntVar(value=0))
    Checkbutton(frame_missing, variable=var_list_members[index],
                text=members[index], command=partial(absent, index, members)).pack(anchor="nw")


frame_remove = tk.Frame()
tk.Label(frame_remove, text="Select Songs to Remove").pack(anchor="nw")

var_list_songs = []
for index, song in enumerate(songs):
    var_list_songs.append(IntVar(value=0))
    Checkbutton(frame_remove, variable=var_list_songs[index],
                text=songs[index], command=partial(remove, index, songs)).pack(anchor="nw")


frame_run = tk.Frame()
button_run = tk.Button(frame_run, text="Run", command=program_run)
button_run.pack(pady=(0, 0))

frame_run_text = tk.Frame()
run_label = tk.Label(frame_run_text, text="(Click to run)")
run_label.pack(pady=(0, 0))

frame_songs_available = tk.Frame()
label_songs_available = tk.Label(frame_songs_available, text="")
label_songs_available.pack(anchor="nw", pady=(0, 0))

frame_notes_and_unavailable = tk.Frame()
label_notes = tk.Label(frame_notes_and_unavailable, text="")
label_notes.pack(anchor="nw", pady=(0, 0))
label_songs_unavailable = tk.Label(frame_notes_and_unavailable, text="")
label_songs_unavailable.pack(anchor="nw", pady=(0, 0))



frame_gig_specs.grid(row=0,column=0, sticky = "nw", padx=(5, 0))
frame_gig_date.grid(row=0,column=1, padx=(5), pady=(0,5))
frame_missing.grid(row=1,column=0, sticky = "nw")
frame_remove.grid(row=1,column=1, sticky = "nw")
frame_run.grid(row=2,column=0, sticky = "nw", padx=(5,0))
frame_run_text.grid(row=3,column=0, sticky = "nw")

frame_songs_available.grid(row=0,column=2, sticky = "nw", padx=(0, 0))
frame_notes_and_unavailable.grid(row=1,column=2, sticky = "nw", padx=(0, 5))

window.mainloop()

"""--------------------------------------------------"""
"""AMITHA SECTION 2 END"""
"""--------------------------------------------------"""