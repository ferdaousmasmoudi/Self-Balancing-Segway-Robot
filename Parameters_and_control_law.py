# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import  scipy.io
import scipy.linalg
from scipy.integrate import odeint

#%% parameters 

t_sim = 5; # Total simulation time [s]

m_wh = 0.058 + 0.2; # MAss of one wheel + mass of 1 motor [kg]

r = 0.5 * 0.085; # Wheel radius [m]

b = 0.255; # Chassis length (along the axle) [m]

a = 0.1; # Chassis width (perpendicular to the axle) [m]

m_plat = 0.081; # mass of 1 wooden platform [kg]

m_bolt = 0.03; # Mass of 1 bolt [kg]

m_0 = 2*m_plat + 4*m_bolt; # total Mass of the body / chassis (excluding wheel and motors) [Kg]

d1 = 0.0325; # distance of the axle from the lower woodden platform [m]

L1 = 0.15; # Length of 1 bolt [m]

L_diag = (a**2 + b**2)**0.5; # Digonal distance of the woodden platform [m]

J_y = 2*(m_plat*a*a/12 + m_plat*(0.5*L1)**2) + 4*(m_bolt*(L1**2)/12 + m_bolt*(0.5*a)**2);

J_z = 2*(m_plat*(a*a + b*b)/12) + 4*(m_bolt * (0.5*L_diag)**2);

J_wh = 0.5*m_wh * r**2; # Moment of inertia of wheel + motor through its axis i.e. 0.5*mr^2 [kgm2] 

l = (m_plat*d1+4*m_bolt*(0.5*L1+d1)+m_plat*(L1+d1))/m_0 ; # Distance of vertical CG of the body from axle [m]

g = 9.8; # Acceleration due to gravity [m/s2]

J5 = J_z + 0.75*m_wh*b**2 + 0.5*m_wh*r*r; # Moment of inertia

M = 2*m_0*m_wh*l*l*r*r + 2*J_wh*m_0*l**2 +  J_y*m_0*r**2 + 2*J_y*m_wh*r**2 + 2*J_wh*J_y;

def lqr(A,B,Q,R):
    """Solve the continuous time lqr controller.
     
    dx/dt = A x + B u
     
    cost = integral x.T*Q*x + u.T*R*u
    """
    #ref Bertsekas, p.151
 
    #first, try to solve the ricatti equation
    X = np.matrix(scipy.linalg.solve_continuous_are(A, B, Q, R))
     
    #compute the LQR gain
    K = np.matrix(scipy.linalg.inv(R)*(B.T*X))
     
    eigVals, eigVecs = scipy.linalg.eig(A-B*K)
     
    return np.array(K), np.array(X), np.array(eigVals)

def dlqr(A,B,Q,R):
    """Solve the discrete time lqr controller.
     
     
    x[k+1] = A x[k] + B u[k]
     
    cost = sum x[k].T*Q*x[k] + u[k].T*R*u[k]
    """
    #ref Bertsekas, p.151
 
    #first, try to solve the ricatti equation
    X = np.matrix(scipy.linalg.solve_discrete_are(A, B, Q, R))
     
    #compute the LQR gain
    K = np.matrix(scipy.linalg.inv(B.T*X*B+R)*(B.T*X*A))
     
    eigVals, eigVecs = scipy.linalg.eig(A-B*K)
     
    return np.array(K), np.array(X), np.array(eigVals)


#%% A and B matrices

A = np.zeros((4,4)); B = np.zeros((4,2))

A[1,0] = 1 ; A[0, 1] = (m_0*r*r+2*m_wh*r*r+2*J_wh)*m_0*l*g / M

A[2,1] = -m_0*m_0*l*l*r*r*g / M

B[0,0] = -(l*m_0*r+m_0*r*r+2*m_wh*r*r+2*J_wh)/M  # motor torques in terms of sum and difference of motor torques

B[2,0] = r*(l*l*m_0+l*m_0*r+J_y)/M; B[3,1] = b/(2*r*J5)

B_mot_torq = np.dot(B, np.array([[1 ,1],[1,-1]])) # Individual motor torques

Q = np.zeros((4,4));
Q[0,0] = 1; # Penalty For Angular velocity
Q[1,1] = 1; # Penalty For Angle
Q[2,2] = 1; # Penalty For Linear velocity
Q[3,3] = 1; # Penalty For turning velocity

R = 100*np.array([[1,0],[0,1]])

K, _, _ = lqr(A,B_mot_torq,Q,R)  


#%% Simulate system using ODE

fs = 100

dt = 1/fs

t_vec = np.arange(0,t_sim,dt)

IC = [0.1, 0.1, 0, 0] # Initial conditions [alpha_dot, alpha, V, theta] 
    
def msd(y,t):
  
    x_dd = np.dot((A - np.dot(B_mot_torq,K)),y)
            
    return x_dd

X_vec = odeint(msd,IC,t_vec)

#%%

plt.plot(t_vec, X_vec[:,2])

y_labs = [r'$\dot\Theta_{y}$ [rad/s]', r'$\Theta_{y}$ [rad]', 'V [m/s]', r'$\Omega_z$ [rad/s]']

for i, j in enumerate(y_labs):
    
    plt.subplot(int(str(22)+str(i+1)))
    
    plt.plot(t_vec, X_vec[:,i])
    plt.ylabel(j, fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.xlabel('T [s]', fontsize = 16)