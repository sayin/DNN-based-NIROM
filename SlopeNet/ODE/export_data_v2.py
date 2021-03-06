#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 17:38:42 2019

@author: Suraj Pawar
"""
import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA

def plot_results_rom(dt1, slopenet, legs):
    filename = slopenet+'_p=0'+str(legs)+'.csv'
    solution = np.loadtxt(open(filename, "rb"), delimiter=",", skiprows=0)
    m,n = solution.shape
    time = solution[:,0]-900
    dt = time[1] - time[0]
    time_test = solution[0:1000,0]-900
    time_pred = solution[1000:,0]-900
    ytrue = solution[:,1:int((n-1)/2+1)]
    ytestplot = solution[0:1000,int((n-1)/2+1):]
    ypredplot = solution[1000:,int((n-1)/2+1):]
    time_test = time[0:1000]
    time_pred = time[1000:]
    for i in range(int(n/2)):
        plt.figure()    
        plt.plot(time,ytrue[:,i], 'r-', label=r'$y_'+str(i+1)+'$'+' (True)')
        plt.plot(time[0:1000],ytestplot[:,i], 'b-', label=r'$y_'+str(i+1)+'$'+' (ML Test)')
        plt.plot(time[1000:],ypredplot[:,i], 'g-', label=r'$y_'+str(1+1)+'$'+' (ML Pred)')
        #plt.plot(solution[:,i+int(n/2)], 'r-', label=r'$y_'+str(i+1)+'$'+' (ML)') 
        plt.ylabel('Response')
        plt.xlabel('Time')
        plt.legend(loc='best')
        name = 'a='+str(i+1)+'.eps'
        #plt.savefig(name, dpi = 400)
        plt.show()
        
def plot_results_lorenz(dt1, slopenet, legs):
    filename = slopenet+'_p=0'+str(legs)+'.csv'
    solution = np.loadtxt(open(filename, "rb"), delimiter=",", skiprows=0)
    m,n = solution.shape
    time = solution[:,0]
    dt = time[1] - time[0]
    time_test = solution[0:1000,0]
    time_pred = solution[1000:,0]
    ytrue = solution[:,1:int((n-1)/2+1)]
    ytestplot = solution[0:1000,int((n-1)/2+1):]
    ypredplot = solution[1000:,int((n-1)/2+1):]
    time_test = time[0:1000]
    time_pred = time[1000:]
    for i in range(int(n/2)):
        plt.figure()    
        plt.plot(time,ytrue[:,i], 'r-', label=r'$y_'+str(i+1)+'$'+' (True)')
        plt.plot(time[0:1000],ytestplot[:,i], 'b-', label=r'$y_'+str(i+1)+'$'+' (ML Test)')
        plt.plot(time[1000:],ypredplot[:,i], 'g-', label=r'$y_'+str(1+1)+'$'+' (ML Pred)')
        #plt.plot(solution[:,i+int(n/2)], 'r-', label=r'$y_'+str(i+1)+'$'+' (ML)') 
        plt.ylabel('Response')
        plt.xlabel('Time')
        plt.legend(loc='best')
        name = 'a='+str(i+1)+'.eps'
        #plt.savefig(name, dpi = 400)
        plt.show()
        
def plot_results_ode(slopenet, legs):
    filename = slopenet+'_p=0'+str(legs)+'.csv'
    solution = np.loadtxt(open(filename, "rb"), delimiter=",", skiprows=0)
    m,n = solution.shape
    for i in range(3):
        plt.figure()    
        plt.plot(solution[:,i], 'b-', label=r'$y_'+str(i+1)+'$'+' (True)') 
        plt.plot(solution[:,i+9], 'r-', label=r'$y_'+str(i+1)+'$'+' (ML)') 
        plt.ylabel('Response')
        plt.xlabel('Time')
        plt.legend(loc='best')
        name = 'a='+str(i+1)+'.eps'
        #plt.savefig(name, dpi = 400)
        plt.show()
    
    for i in range(3,6):
        plt.figure()    
        plt.plot(solution[:,i], 'b-', label=r'$y_'+str(i+1)+'$'+' (True)') 
        plt.plot(solution[:,i+9], 'r-', label=r'$y_'+str(i+1)+'$'+' (ML)') 
        plt.ylabel('Response')
        plt.xlabel('Time')
        plt.legend(loc='best')
        name = 'a='+str(i+1)+'.eps'
        #plt.savefig(name, dpi = 400)
        plt.show()
    
    for i in range(6,9):
        plt.figure()    
        plt.plot(solution[:,i], 'b-', label=r'$y_'+str(i+1)+'$'+' (True)') 
        plt.plot(solution[:,i+9], 'r-', label=r'$y_'+str(i+1)+'$'+' (ML)') 
        plt.ylabel('Response')
        plt.xlabel('Time')
        plt.legend(loc='best')
        name = 'a='+str(i+1)+'.eps'
        #plt.savefig(name, dpi = 400)
        plt.show()

def plot_results_lorenzold(slopenet, legs):
    filename = slopenet+'_p=0'+str(legs)+'.csv'
    solution = np.loadtxt(open(filename, "rb"), delimiter=",", skiprows=0)
    m,n = solution.shape
    for i in range(3):
        plt.figure()    
        plt.plot(solution[:,i], 'b-', label=r'$y_'+str(i+1)+'$'+' (True)') 
        plt.plot(solution[:,i+3], 'r-', label=r'$y_'+str(i+1)+'$'+' (ML)') 
        plt.ylabel('Response')
        plt.xlabel('Time')
        plt.legend(loc='best')
        #name = 'a='+str(i+1)+'.eps'
        #plt.savefig(name, dpi = 400)
        plt.show()
    
       
def calculate_l2norm(ytest_ml, testing_set, m, n, legs, slopenet, problem, y2s=0.0):
    # calculates L2 norm of each series
    error = testing_set-ytest_ml
    l2norm_sum = 0.0
    l2norm_true = 0.0
    l2norm_nd = 0.0
    for i in range(n-1):
        l2norm_sum += LA.norm(error[:,i])
        
    for i in range(n-1):
        l2norm_true += LA.norm(testing_set[:,i])
    
    l2norm_nd = l2norm_sum/l2norm_true
    
    rmse = l2norm_sum/np.sqrt(m)
    
    list = [legs, slopenet, problem, l2norm_nd, l2norm_sum, l2norm_true, y2s, rmse]
    with open('l2norm.csv', 'a') as f:
        f.write("\n")
        for item in list:
            f.write("%s\t" % item)
        
    return l2norm_sum, l2norm_nd

def export_results_rom(ytest_ml, testing_set, time, m, n, slopenet, legs):
    # export result in x y format for further plotting
    filename = slopenet+'_p=0'+str(legs)+'.csv'
    time = time.reshape(m,1)
    results = np.hstack((time, testing_set, ytest_ml))
    np.savetxt(filename, results, delimiter=",")
    
def export_results_ode(ytest_ml, testing_set, m, n, slopenet, legs):
    # export result in x y format for further plotting
    filename = slopenet+'_p=0'+str(legs)+'.csv'
    results = np.hstack((testing_set, ytest_ml))
    np.savetxt(filename, results, delimiter=",")
    
