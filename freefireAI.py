import cv2
import torch
import numpy as np
import pandas
import mss
import win32api
import time
import pyautogui
import asyncio
import math

#kpx = 1/8 kpy = 1/15 ki = ? kd = ?
def pid(ix, epx, iy, epy, dx, dy, dt, kpx, kix, kdx, kpy, kiy, kdy):
    print(f'vars{ix, epx, iy, epy, dx, dy, dt, kpx, kix, kdx, kpy, kiy, kdy}')
    dt = dt*3000
    if(ix > 320000):
        ix = 250000
    if(iy > 210000):
        iy = 170000
    ex, ey = math.sqrt(dx*dx), math.sqrt(dy*dy)
    if dx < 0 and dy < 0:
        dx, dy = -1*int(kpx*ex+kix*(ix+ex*dt)+kdx*(ex-epx)/dt) , -1*int(kpy*ey+kiy*(iy+ey*dt)+kdy*(ey-epy)/dt)
    elif dx > 0 and dy < 0:
        dx, dy = int(kpx*ex+kix*(ix+ex*dt)+kdx*(ex-epx)/dt), -1*int(kpy*ey+kiy*(iy+ey*dt)+kdy*(ey-epy)/dt)
    elif dx < 0 and dy > 0 :
        dx, dy = -1*int(kpx*ex+kix*(ix+ex*dt)+kdx*(ex-epx)/dt), int(kpy*ey+kiy*(iy+ey*dt)+kdy*(ey-epy)/dt)
    else:
        dx, dy = int(kpx*ex+kix*(ix+ex*dt)+kdx*(ex-epx)/dt), int(kpy*ey+kiy*(iy+ey*dt)+kdy*(ey-epy)/dt)
    ix, iy = ix + ex*dt, iy+ey*dt
    epx, epy = ex, ey
    return ix, epx, iy, epy, dx, dy

def update_enemies_list(x,y, enemieslist):
    for enemy in enemieslist:
        xc, yc = enemy 
        if x-10 <= xc <= x+10 and y-10 <= yc <= y+10:
            locked_enemy = enemy
            return locked_enemy
    return None

def sort_enemies(enemieslist):
    for i in range(len(enemieslist)):
        xi,yi = enemieslist[i]
        for j in range(i+1, len(enemieslist)):
            xj, yj = enemieslist[j]
            if(xi < xj):
                temp = xi
                xi = xj
                xj = temp
    return enemieslist

def detect(detect_feed, src, enemieslist):
    outputs = model(detect_feed)
    bbox = outputs.pandas().xyxy[0]
    for i, row in bbox.iterrows():
        if(row[4] < 0.5):
            continue
        x0, y0, x1, y1 = int(row[0]), int(row[1]), int(row[2]), int(row[3])
        #offset from crop
        x0,y0,x1,y1 = x0+(int(left)), y0+(int(top)), x1+(int(left)), y1+(int(top))
        cv2.rectangle(src, (x0,y0), (x1, y1), [0,255,0], 1)
        centerx = (x0 + x1) // 2
        centery = (y0 + y1) // 2
        #print(f'x{centerx} y{centery}')
        cv2.circle(src, (centerx, centery), 5, [0, 0, 255])
        cv2.line(src, (aimx, aimy), (centerx, centery), [0,255,0], 2)
        enemieslist.append((centerx,centery))
    return enemieslist

model_pth = 'C:/Users/harrisonc/Downloads/best.pt'
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = torch.hub.load("WongKinYiu/yolov7","custom",f"{model_pth}",trust_repo=True)

while True:
    a = win32api.GetKeyState(0x26)  # press up arrow key to start 
    if a < 0:
        break

aimx,aimy = 590, 366
left, top = aimx - 160, aimy - 170
enemieslist= []
ix, epx, iy, epy = 250000,0,170000,0
canshoot=True
lastshot = 2.5

stime = time.time()
while True:
    with mss.mss() as sct:
        monitor = {"top":0, "left":0, "width":1180, "height":700}
        src = np.array(sct.grab(monitor))
        cropped = {"top":top, "left":left, "width":320, "height":320}
        detect_feed = np.array(sct.grab(cropped))
    
    detect_feed = cv2.cvtColor(detect_feed, cv2.COLOR_RGB2GRAY)
    enemieslist = detect(detect_feed, src, enemieslist)

    dt = time.time() - stime
    stime = time.time() 

    if enemieslist:
        sort_enemies(enemieslist)
        x,y = enemieslist.pop(0)
        dx, dy = x-aimx, y-aimy
        if abs(dx) < 10 and abs(dy) < 10 and canshoot:
            lastshot = time.time() 
            canshoot = False
            pyautogui.leftClick(_pause = None)
        ix, epx, iy, epy, dx, dy = pid(ix, epx, iy, epy, dx, dy, dt, 1/25, 1/200000, 6, 1/40, 1/200000, 6)
        cursorx, cursory = win32api.GetCursorPos()
        pyautogui.moveTo(cursorx+dx, cursory+dy, duration=0.075, _pause=False)
    
    st = time.time() - lastshot

    if not canshoot and st > 2.5:
        canshoot = True
    
    #print(win32api.GetCursorPos())
    cv2.circle(src,(aimx,aimy), 1, [0,255,0], 2)
    cv2.imshow("src", src)
    cv2.imshow("detectionfeed", detect_feed)
    
    a = win32api.GetKeyState(0x28)
    if cv2.waitKey(1) == ord('q') or a < 0:
        cv2.destroyAllWindows()
        break
print('Done.')

