# Código de cinemática inversa para o manipulador Barrett-WAM com 4 graus de liberdade
# 4 juntas rotativas
# Cinemática Inversa calculada manualmente
import numpy as np


def	juntas(px,py,pz):
    la = 0.55
    lc = 0.35
    
    q1 = np.arctan2(py,px)
    q3 = 0
    q4 = np.arcsin(((px*np.cos(q1) + py*np.sin(q1))**2+(-pz)**2 -lc**2 - la**2)/(-2*la*lc))
    
    c1 = lc*np.cos(q4)
    c2 = la - lc*np.sin(q4)
    c3 = px*np.cos(q1)+py*np.sin(q1)
    c4 = -pz
    sin_q2 = ((c4 + c2*c3/c1)/(c2*c2/c1 + c1))
    cos_q2 = (c3-c2*sin_q2)/c1
    
    q2 = np.arctan2(sin_q2,cos_q2)
    
    return q1,q2,q3,q4
    
resultado = juntas(-0.292,0.38,0.051)
print(resultado[0]*180/np.pi,resultado[1]*180/np.pi,resultado[3]*180/np.pi,)
