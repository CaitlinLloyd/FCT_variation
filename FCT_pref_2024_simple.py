### Food Choice Python version is updated in June 2024
### by Xinwei Samantha Han (RA at Columbia Center for Eating Disorders)
### Based on Food Choice Task Matlab Version(2016) by Dr. Karin Foerde and Dr. Joanna Steinglass
### Python version was created by Serena J. Gu (RA) on Nov.18 2022

from fct_library import *


import os
import re
import glob
from psychopy import visual, core, data, logging, gui
from psychopy.hardware.emulator import launchScan
import numpy as np
import pandas as pd
import constants
import psychopy
import random
import itertools
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

    #########################Experiment Imformation########################
    # psychopy.useVersion('2022.2.4')
expName = 'FCT_pref_2024_simple'

expInfo = {'participant': '', 'TR': 2.000, 'volumes': 300, 'sync': 't','block': 'preference',
                   'time point (enter number only)': '', 'order': 'Condition_1_C'}
MR_settings = {'TR': expInfo['TR'], 'volumes': expInfo['volumes'], 'sync': expInfo['sync'], 'skip': 3}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel

        # validate input for time point
time_pt_str = expInfo['time point (enter number only)']
time_pt_val = None

try:
    time_pt_val = int(time_pt_str)
except ValueError:
    print()
    error_msg = "Please only enter a number for time point (eg. 1, 2...)"
    error_dlg = gui.Dlg(title="Error")
    error_dlg.addText(error_msg)
    error_dlg.show()
        
if time_pt_val is not None:
    time_pt = 'T' + str(time_pt_val)
else:
    print("missing time point value")

        # validate input for excluding reference food
#foodlist = constants.FOODLIST


ITI_list=[3, 5, 2, 6, 4, 5, 3, 7, 2, 5, 4, 6, 3, 5, 2, 8, 4, 6, 3, 5,7, 2, 6, 4, 5, 3, 7, 2, 6, 4, 5, 3, 6, 2, 7, 5, 4, 6, 3, 8,5, 7, 4, 6, 3, 10, 5, 9, 6, 12,3,7]

random.shuffle(ITI_list)
list_1=ITI_list.copy()
random.shuffle(ITI_list)
list_2=ITI_list.copy()
random.shuffle(ITI_list)
list_3=ITI_list.copy()
random.shuffle(ITI_list)
list_4=ITI_list.copy()
    
lists=[list_1,list_2,list_3,list_4]


expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
test_block = expInfo['block']
    #print(f"#################################{expInfo}")

    # read input files
order_list = f"{_thisDir}/order/{expInfo['order']}.xlsx"
f_list = f"{_thisDir}/lists/HF_LF_60.csv"


fList = pd.read_csv(f_list)
## split list into two with 30 HF and 30 LF items per list; each food presented twice in 2 blocks (i.e., four presentations total)
low=fList[fList.fat==0]
high=fList[fList.fat==1]
low1=low.sample(frac=.5)
low2=low[~low['food'].isin(low1['food'])]
high1=high.sample(frac=.5)
high2=high[~high['food'].isin(high1['food'])]
group1=high1.append(low1)
group2=high2.append(low2)
group1=group1.append(group1)
group2=group2.append(group2)
group1=group1.sample(frac=True)
group2=group2.sample(frac=True)
group3=group1.sample(frac=True)
group4=group2.sample(frac=True)
groups=[group1,group2,group3,group4]

order = pd.read_excel(order_list)
cond = re.findall(r'\d+', expInfo['order'])
condition = int(cond[0])
# condition == 1 -> ratings will not be reversed(0); condition == 2 -> ratings will be reversed(1)
rating_reversed = 0 if condition == 1 else 1


    #########################Experiment Start########################
win = visual.Window(fullscr=True, winType='pyglet', monitor="testMonitor",
                        units="height", color="#000000", colorSpace='hex', blendMode="avg")
win.mouseVisible = False
    
welcome_text = newText(win, "welcome_text","Welcome!")
welcome_text.draw()
win.flip()
newKey(keyList=['space'])

def get_food_name(food_full):
    return ' '.join(re.findall(r'/([\w .\& .\%]+).jpg', food_full))

# read from existing health and taste rating file
def read_file():
    pattern = f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_choice_{group_num}.csv"
        # check if we found any files with the pattern
    matching_files = glob.glob(pattern)
    if matching_files:
        input_df = pd.read_csv(matching_files[0])
    # print(matching_files)
    else:
        print("No rating file found for this participant.")
        return None
    return matching_files[0], input_df

  
def get_rating(order_row, existed_file):
    newInstruction(win, "inst1", order_row, keyList=['1', 'space'])
    newInstruction(win, "inst2", order_row, keyList=['1', 'space'])
    newInstruction(win, "inst3", order_row, keyList=['1', 'space'])
    foodList=pd.read_csv(existed_file)
    duration = expInfo['volumes'] * expInfo['TR']
    
    event.clearEvents()
    globalClock = core.Clock()
    vol = launchScan(win, MR_settings, globalClock=globalClock, wait_msg='loading...')
    globalClock.reset()
    #event.waitKeys(keyList =['t'])
    get_ready = newTextWait(win, "ready", constants.GETREADY)
        #start_time = core.getTime()
        #create timing array
    # preload all images before block starts
    image_cache = {}
    for _, food in foodList.iterrows():
        food_name = food['food']
        img_path = f"{_thisDir}{food_name}"
        image_cache[food_name] = visual.ImageStim(win, image=img_path, units='height',size=0.75)
    blockClock=core.Clock()
    for index, food in foodList.iterrows():
        food_name = food['food']
        trial_start = food['trialstart']
        start_cross = blockClock.getTime()
        abs_iti_onset = globalClock.getTime()
        logging.data(f"Trial {index} | ITI onset: {start_cross:.4f} | abs ITI onset: {abs_iti_onset:.4f} | food: {food_name}")
        while blockClock.getTime() < trial_start:
            newCross(win)
        image_onset = blockClock.getTime()
        abs_onset = globalClock.getTime()
        image_cache[food_name].draw()
        win.flip()
        logging.data(f"Trial {index} | Stim onset: {image_onset:.4f} | abs onset: {abs_onset:.4f}")
        core.wait(2.5)
        #showImageWait(win, f"{_thisDir}{food_name}", zoom=1.5)
        key = showImageRate(win, order_row['rating'], zoom=1)
        if key is None:
            win.flip()
            key = [['0'], None]
            corrected_rating = None
            p_resp="Missed Trial"
        else:
            corrected_rating = int(key[0][0]) if condition == 1 else 6 - int(key[0][0])
            p_resp=str(corrected_rating)
        logging.data(f"Trial {index} | Response: {p_resp} | RT: {key[1]}")
        logging.flush()
        showResp(win,p_resp,zoom=2)
        temp_list = (key[0][0], key[1],corrected_rating, image_onset, abs_onset)
        temp_index = index #output_df[output_df['food_item'] == get_food_name(food_name)].index
        output_df.loc[temp_index, ['pref_recorded_response', 'pref_rt', 'pref_rating', 'image_onset','abs_onset']] = temp_list
        output_df.to_csv(f"{save_choice}_{group_num}.csv", index=False) if existed_file is None else output_df.to_csv(existed_file, index=False)
    end_of_block = newText(win, "end_of_block", constants.ENDOFBLOCK)
    end_of_block.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    win.flip()

p_trial_l=[6]*52
p_trial_l[0]=0


block=0

for group in groups:
    ITI=lists[block]
    onset=np.add(ITI, p_trial_l)
    onset=list(itertools.accumulate(onset))
    block=block+1
    group_num=f"block_{block}"
    output=[]
    group['ITI']=ITI
    group['p_tri_l']=p_trial_l
    group['rel_start']=onset
    logname= f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_{expInfo['date']}_block_{block}"
    logging.LogFile(logname+'.log', level=logging.DATA)
    logging.console.setLevel(logging.WARNING)
    logging.exp(f"=== Block {block} started ===")
    if read_file() is None: 
        i=0
        for _, food in group.iterrows():
            new_row = {
            'trial': i,
            'food': "/stimuli/"+food['food'],
            'food_item': get_food_name(food['food']),
            'fat': food['fat'],
            'available': food['available'],
            'hilo': food['hilo'],
            'SubID': expInfo['participant'],
            'time point': time_pt,
            'date': expInfo['date'][0:10],
            'condition': condition,
            'rating_reversed': rating_reversed,
            'block': block,
            'trialstart':food['rel_start']
            }
            output.append(new_row)
            i=i+1
        output_df = pd.DataFrame(output)
        output_df.to_csv(f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_choice_{group_num}.csv", index=False)
        existed_file,output_df = read_file()
    else:
        existed_file,output_df = read_file()

    for i, row in order.iterrows():
        get_rating(row, existed_file)
        logging.exp(f"=== Block {block} ended ===")




    ########################## Saving Logging Files #########################


search_pattern = os.path.join(f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_choice*")
matching_files = glob.glob(search_pattern)
    
all_df = []
block_num=0
for f in matching_files:
    block_num=block_num+1
    df = pd.read_csv(f)
    all_df.append(df)
        
combined_df = pd.concat(all_df, ignore_index=True)
combinedoutputfile=f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_{expInfo['date']}_all.csv"
combined_df.to_csv(combinedoutputfile, mode='a', header=False, index=False)


win.close()
core.quit()
