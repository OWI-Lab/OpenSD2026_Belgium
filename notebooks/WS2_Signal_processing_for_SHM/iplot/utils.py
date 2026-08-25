import numpy as np

def calcW_n(k:float,m:float):
    w_n = np.sqrt(k/m)
    return w_n

def impulse_response(m:float,c:float,k:float,t:np.ndarray):
    xi=calcXi(m=m, c=c, k=k) 
    w_n=calcW_n(m=m, k=k) 
    w_d= calcW_d(w_n, xi) 
    h=1/(m*w_d)*np.exp(-xi*w_n*t)*np.sin(w_d*t)
    return h

def calcW_d(w_n:float,xi:float):
    w_d = w_n*np.sqrt(1-xi**2)
    return w_d

def calcXi(m:float, c:float, k:float):
    xi= c/(2*np.sqrt(m*k))
    return xi

def convert_pulsation(w:float):
    f = w/2/np.pi
    return f

def harmonic_force(f:float, t:float):
    w_f = f*np.pi*2
    force = np.sin(w_f*t)
    return force
def harmonic_response(m:float,c:float,k:float,f:np.ndarray,t:np.ndarray):
    f = harmonic_force(f, t)
    h = impulse_response(m=m, c=c, k=k, t=t)
    
    response = np.convolve(h, f, mode='full') 
    
    return response[:len(f)]

def frequency_response_function(m:float,c:float,k:float,f:np.ndarray):

    w = np.pi*2*f
    wn = calcW_n(m=m,k=k)
    xi = calcXi(m=m,c=c,k=k)
    H=1/(m*(wn**2-w**2+2j*xi*w*wn))
    return H
