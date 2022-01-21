import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

#KP = 4.5
#KI = 0.85
#KD = 0.75
KP = 0.8
KI = 0.3
KD = 0.1


#control = 1
#R = 100
k = 1
print("input of PID controller type")
print("1:PID velocity controller, 2:PID position controller")
control = int(input('intpu PID controller type:')) #1,2
print("목표값(설정치)를 입력 하시오:")
R = int(input('목표값 입력:'))#100, 15, 200
U_2 = Y_1 = 0
e_3 = e_2 = e_1 = 0
#//R = 200;
sum_Y = 0
numb_val_plt = []
plant_val_plt = []
cont_val_plt = []

for i in range(1, 401, 1):
    
    if control == 1:
        U_1 = U_2 + KP * (e_1 - e_2) + KI * e_1 + KD * (e_1 - 2 * e_2 + e_3) # 제어기 제어값
        Y = 0.77 * Y_1 + 0.322 * U_1 + 0.111 *U_2 #//가상 플랜트
        e = R - Y #오차값
        # py = 430 - Y / 10;
        py = Y # Plant 출력값
    
    if i == 400 * k:
        ii = i - 400 * k
        pt_1 = 30
        k = k + 1
        
    elif i > 400 * (k - 1):
        ii = i- 400 * (k - 1)
    
    else:
        ii = i
        
    pt = 30 + ii
    
    pr = R
    pu = U_1
    py = Y
    
    if i == 100:
         Y = Y * 1.05 #외란 인가
    #elif i == 200:
        #R = 150 #설정값 변경
        
    e_3 = e_2
    e_2 = e_1
    e_1 = e
    U_2 = U_1
    Y_1 = Y
    pt_1 = pt
    pr_1 = pr
    pu_1 = pu
    
    print("횟수:", i, "목표값:", R, "제어기기출력:", U_1, "플랜트 출력:", Y)
    
    numb_val_plt.append(i)
    plant_val_plt.append(Y)
    cont_val_plt.append(U_1)
    
plt.plot(numb_val_plt, plant_val_plt)
plt.plot(numb_val_plt, cont_val_plt)
plt.grid(True) #x, y축 줄표시
plt.legend(("Control Value")) #범례표시
#plt.axis([0, 20, -100, 100]) #x, y축 크기설정
plt.ylabel("plnat, Controller Output") #y축에 해당문자열 표시
plt.show()         