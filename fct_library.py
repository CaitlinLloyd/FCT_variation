from psychopy import visual, event, core
from psychopy.hardware import keyboard
from random import uniform
from psychopy.event import Mouse

def newText(win, name, text, height=0.035, pos=(0, 0)):
    return visual.TextStim(win=win, name=name,
        text=text, font='Arial', pos=pos, height=height, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, languageStyle='LTR', depth=0.0)

    
def newTextQuest(win, text, height=0.035, pos=(0, 0)):
    return visual.TextStim(win=win, 
        text=text, font='Arial', pos=pos, height=height, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, languageStyle='LTR', depth=0.0)

def notnewKey(keyList=None, maxWait=float('inf')):
    #print(f"newKey(keyList={keyList},maxWait={maxWait})")
    key = None
    if keyList is None:
        key = event.waitKeys(maxWait=maxWait)
        keyList = ['escape', 'shift', 'return']
    else:
        for exit_key in ['escape', 'shift', 'return']:
            if exit_key not in keyList:
                keyList.append(exit_key)
        key = event.waitKeys(keyList=keyList, maxWait=maxWait)
    if key is not None and 'escape' in key and 'shift' in key and 'return' in key:
        core.quit()
    return key


def newKey(keyList=None, maxWait=float('inf')):
    # print(f"newKey(keyList={keyList},maxWait={maxWait})")
    key = None
    if keyList is None:
        key = event.waitKeys(maxWait=maxWait)
    else:
        if 'escape' not in keyList:
            keyList.append('escape')
        key = event.waitKeys(keyList=keyList,maxWait=maxWait)
    if key is not None and 'escape' in key:
        keyList_exit = keyList + ['return']
        if newKey(keyList=keyList_exit)=="EXIT":
            core.quit() # program will exit after pressing "escape" and "return" consecutively
    if key is not None and 'return' in key:
        return "EXIT"
    return key


def timedKey(callback, keyList=None, maxWait=4.0):
    remainder = maxWait
    clock = core.getTime()
    key = event.waitKeys(keyList=keyList, maxWait=remainder)
    pressTime = float('inf')
    if key is not None:
        pressTime = core.getTime() - clock
        callback()
    else:
        return None
    remainder = maxWait - pressTime
    core.wait(remainder)
    return key, pressTime
    
def NOtimedKey(keyList=None):
    clock = core.getTime()
    key = event.waitKeys(keyList=keyList)
    pressTime = float('inf')
    if key is not None:
        pressTime = core.getTime() - clock
        #callback()
    else:
        return None
    return key, pressTime

def slider_rating(slider):
    key = slider.getRating()
    RT=slider.getRT()
    #posit= slider.markerPos()
    return key, RT

def newImage(win, image=None, zoom=1.0, pos=(0, 0.2)):
    image = visual.ImageStim(
        win=win,
        name='image', units='norm', 
        image=image, mask=None,
        ori=0, pos=pos, size=None,
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=512, interpolate=True, depth=0.0)
    sz = image.size
    image.setSize((sz[0] * zoom, sz[1] * zoom))
    return image


def newInstruction(win, name, row, keyList=None):
    inst1 = newText(win, name, row[name])
    inst1.draw()
    win.flip()
    newKey(keyList=keyList)


def newCross(win,wait_time):
    cross = visual.ShapeStim(
        win=win, name='fixationcross', vertices='cross',
        size=(0.035, 0.035),
        ori=0.0, pos=(0, 0),
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=0.0, interpolate=True)
    cross.draw()
    win.flip()
    core.wait(wait_time)


def newTextWait(win, name, text, wait_time=8.0, height=0.035, pos=(0, 0)):
    textwait = visual.TextStim(win=win, name=name,
        text=text, font='Arial', pos=pos, height=height, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, languageStyle='LTR', depth=0.0)
    textwait.draw()
    win.flip()
    #wait_time = uniform(0.3, 0.5)
    core.wait(wait_time)

def array_create(frame):
    length=len(frame)
    arr=[0]
    for _ in range(1, length):
        increment = uniform(9.0,11.0)
        arr.append(arr[-1] + increment)
    return arr
    

def showImageWait(win, img_path, wait_time=3.0, pos=(0, 0.0), zoom=1.5):
    image1 = newImage(win, image=img_path, zoom=zoom, pos=pos)
    image1.draw()
    win.flip()
    core.wait(4.0)
    

def showImageRate(win, rating, wait_time=2.5, keyList=['1','2','3','4','5'], pos=(0, 0.2), ref_image=None, ref_image_pos=(-0.35, 0.2),zoom=1):
    question = newTextQuest(win, "How much do you want to eat this item?", pos=(0, 0.2))
    rating = newText(win, "rating", rating, pos=(0, -0.2))
    question.draw()
    rating.draw()
    win.flip()
    def disableRating():
        question.draw()
        win.flip()
    return timedKey(disableRating, keyList=keyList, maxWait=wait_time)

def showResp(win,response,zoom=4):
    text = newText(win, "p_resp",response, pos=(0, 0),height=0.2)
    text.draw()
    win.flip()
    core.wait(0.5)
    
    
    
def showImageRateBehav(win,img_path, quest, scale, keyList=['1','2','3','4','5'], zoom=1.5):
    image1 = newImage(win, image=img_path, zoom=zoom, pos=(0, -0.05))
    image1.draw()
    question = newText(win, 'quest',quest, pos=(0, 0.35))
    #rating = newText(win, "rating", rating, pos=(0, -0.2))
    question.draw()
    scale_text= newText(win, 'scale',scale, pos=(0, -0.4))
    scale_text.draw()
    #rating.draw()
    win.flip()
    return NOtimedKey(keyList=keyList)
    

