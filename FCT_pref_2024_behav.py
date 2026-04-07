### This rating task is based on the FCT that was developed by Dr. Karin Foerde and Dr. Joanna Steinglass
### and updated by Serena Gu and Xinwei Samantha Han 


from fct_library import *

def run():
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
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    #########################Experiment Imformation########################
    # psychopy.useVersion('2022.2.4')
    expName = 'FCT_pref_2024'
    while True:
        expInfo = {'participant': '',
                   'block': ['all'],'order': ['Condition_all_nutrients','Condition_all_nutrients_rev'],
                   'h_list': ['HF_LF_60'],'condition':['forward','reverse'],
                   'time point (enter number only)': ''}
        dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
        if dlg.OK == False:
            print(expInfo)
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
            if error_dlg.OK:
                continue       
        if time_pt_val is not None:
            time_pt = 'T' + str(time_pt_val)
        else:
            print("missing time point value")

        # validate input for excluding reference food
        foodlist = constants.FOODLIST
        break


    # save experiment info
    expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName
    test_block = expInfo['block']
    #print(f"#################################{expInfo}")

    # read input files
    order_list = f"{_thisDir}/order/{expInfo['order']}.xlsx"
    h_list = f"{_thisDir}/lists/{expInfo['h_list']}.csv"
    hList = pd.read_csv(h_list)
    ## split list into two with 20 HF and 20 LF items per list; each food presented twice in 2 blocks (i.e., four presentations total)
    #hList= hList.sample(frac=True)
    order = pd.read_excel(order_list)
    cond = expInfo['condition']
    condition = cond
    # condition == 1 -> ratings will not be reversed(0); condition == 2 -> ratings will be reversed(1)
    rating_reversed = 0 if condition =='forward' else 1

    #########################Saving Data File Info########################
    save_all = f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_{expInfo['date']}_all"
    save_filename = f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_{expInfo['date']}_behav"
    save_choice = f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_{expInfo['date']}_rating"
    save_foodtask = f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_{expInfo['date']}_ratingtask"

    logFile = logging.LogFile(save_all+'.log', level=logging.DEBUG)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    output = []
    columns = ['food_item', 'SubID', 'time point', 'date','pref_recorded_response',
               'pref_rating', 'pref_rt', 'image_onset',
               'available', 'fat', 'hilo', 'rating_reversed','block']
    output_df = pd.DataFrame(output, columns=columns)

    #########################Experiment Start########################
    win = visual.Window([1440, 900], fullscr=True, winType='pyglet', monitor="testMonitor",
                        units="height", color="#000000", colorSpace='hex', blendMode="avg")
    win.mouseVisible = False
    
    welcome_text = newText(win, "welcome_text", "Welcome!")
    welcome_text.draw()
    win.flip()
    newKey(keyList=['space'])

    def get_food_name(food_full):
        return ' '.join(re.findall(r'/([\w .\& .\%]+).jpg', food_full))

    def read_file():
        # read from existing health and taste rating file
        pattern = f"{save_choice}_{block_type}.csv"
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
        foodList = hList_sample
        globalClock = core.Clock()
        # event.waitKeys(keyList =['t'])
        start_time = core.getTime()
        print(output_df)
        trial_start=0
        for index, food in output_df.iterrows():
            food_name = _thisDir + "/stimuli/" + food['food_item']
            start_cross = core.getTime() - start_time
            newCross(win, wait_time=1)
            image_onset = core.getTime() - start_time
            key = showImageRateBehav(win, food_name, quest=quest,scale=scale, zoom=1.5)
            corrected_rating = key[0]
            temp_list = (get_food_name(food_name),key[0], key[1])
            #temp_index = output_df[output_df['food_item'] == get_food_name(food_name)].index
            #print(temp_index)
            print(food_name)
            output_df.loc[index, ['food_item','pref_recorded_response', 'pref_rt']] = temp_list
            output_df.to_csv(f"{save_choice}_{block_type}.csv", index=False) if existed_file is None else output_df.to_csv(existed_file, index=False)
            #trial_start = core.getTime() + uniform(0.3,0.5)
        end_of_block = newText(win, "end_of_block", constants.ENDOFBLOCK)
        end_of_block.draw()
        win.flip()
    
    block_num=0

    order=order.sample(frac=1)
    for i, row in order.iterrows():
        output=[]
        output_df=None
        block_type=order.loc[i][1]
        scale=order.loc[i][5]
        quest=order.loc[i][6]
        hList_sample=hList.sample(frac=1)
        if read_file() is None:
            for _, food in hList_sample.iterrows():
                print(food)
                new_row = {
                'food_item': food['food'],#get_food_name(food['food']),
                'fat': food['fat'],
                'available': food['available'],
                'hilo': food['hilo'],
                'SubID': expInfo['participant'],
                'time point': time_pt,
                'date': expInfo['date'][0:10],
                'condition': condition,
                'rating_reversed': rating_reversed,
                }
                output.append(new_row)
                output_df = pd.DataFrame(output, columns=columns)
                #output_df['rating_type']=block_type
                output_df.to_csv(f"{save_choice}_{block_type}.csv", index=False)
                existed_file, output_df = read_file()
        else:
            existed_file, output_df = read_file()
        get_rating(row, existed_file)
        

    win.close()
    core.quit()
