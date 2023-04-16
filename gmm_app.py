# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 11:00:52 2023

@author: gardi
"""

import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os
import numpy as np
from sklearn.mixture import GaussianMixture as GMM
from sklearn.model_selection import GridSearchCV
import pandastable as pt
from tkinter import messagebox
 

root= tk.Tk()
root.title('GMM application')

canvas1 = tk.Canvas(root, width = 600, height = 300)
canvas1.pack()
 
label1 = tk.Label(root, text='Calcium Imaging GMM alapvonal', bg='snow')
label1.config(font=('Helvetica', 20))


canvas1.create_window(300, 50, window=label1)
canvas1.configure(bg='snow')

canvas1.create_text(300, 100, text="készítette: Gárdi Réka Lorin", fill="black", font=('Helvetica', 12))
canvas1.create_text(300, 120, text="2023", fill="black", font=('Helvetica', 10))
canvas1.pack()


def getExcel ():
      global df
      global maximumok
      global import_file_path

      import_file_path = filedialog.askopenfilename()
      df = pd.read_csv (import_file_path)
      beadas = int(os.path.basename(import_file_path).split('-')[-1].split('.')[0])
      df_reaction = df[beadas:(beadas+50)]
      df_reaction.drop(df_reaction.index[-1], axis=0, inplace=True)
      df_reaction.drop(['Frame'], axis=1, inplace=True)
      maximumok = np.amax(df_reaction, axis=0)
      df.drop(df.index[beadas:len(df)], axis=0, inplace=True)
      df.drop(['Frame'], axis=1, inplace=True)
      messagebox.showinfo("info","A fájl sikeresen fel lett töltve.")

def getGMM ():
    global df_gmm
    
    tuned_parameters = {'n_components': np.array([1,2,3,4,5,6])}
    list_opt_n_components = []
    clf = GridSearchCV(GMM(random_state=10),tuned_parameters,cv=10,n_jobs=7)
    for column in df:
        list_opt_n_components.append(column)
        clf.fit(df[column].to_numpy().reshape(-1, 1))
        sorszam = np.argmin(clf.cv_results_['rank_test_score'])
        list_opt_n_components.append(sorszam+1)
        list_opt_n_components.append(clf.cv_results_['mean_test_score'][sorszam])
    n_comp = pd.DataFrame({
        "ROI": [list_opt_n_components[::3]],
        "n": [list_opt_n_components[1::3]],
        "neg_log_likelihood": [list_opt_n_components[2::3]]
    })
    A = pd.DataFrame(n_comp['ROI'].to_list())
    B = pd.DataFrame(n_comp['n'].to_list())
    C = pd.DataFrame(n_comp['neg_log_likelihood'].to_list())

    opt_n_comp = pd.concat([A, B, C]).transpose()
    opt_n_comp.columns = ['ROI', 'M', 'neg_log_likelihood']

    df_opt_n_comp = pd.DataFrame(opt_n_comp)
    
    list_final = []
    list_sorszam_weights_final = []
    list_sorszam = range(len(df.columns))

    for i in list_sorszam:
        gmm = GMM(n_components = opt_n_comp['M'][i], max_iter=1000, random_state=10, covariance_type = 'full')
        list_final.append(gmm.fit(np.array(df.iloc [:, [i]]).reshape(-1, 1)).means_)
        list_sorszam_weights_final.append(np.argmax(gmm.fit(np.array(df.iloc [:, [i]]).reshape(-1, 1)).weights_))
    

    list_alapvonal = []

    for i in list_sorszam:
        list_alapvonal.append(list_final[i][list_sorszam_weights_final[i]])

    df_alapvonal = pd.DataFrame(list_alapvonal)
    df_alapvonal.columns = ['gmm_baseline']

    df_gmm = df_opt_n_comp
    df_gmm['gmm_baseline'] = df_alapvonal['gmm_baseline']
    df_gmm['max_value'] = maximumok.tolist()    
    df_gmm['reaction'] = df_gmm['max_value']/df_gmm['gmm_baseline']
    
    dTDa1 = tk.Toplevel()
    
    nev = os.path.basename(import_file_path).split('.')[0]
    
    dTDa1.title(f"gmm_output_{nev}")
    dTDaPT = pt.Table(dTDa1, dataframe=df_gmm, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()
    
def export():
    nev = os.path.basename(import_file_path).split('.')[0]
    
    df_gmm.to_excel(f"gmm_output_{nev}.xlsx")    
    messagebox.showinfo("info","A táblázat exportálásra került.")
      
browseButton_Excel = tk.Button(text='1. Fájl betöltése', command=getExcel, bg='SteelBlue1', font=('Helvetica', 12, 'bold'))
canvas1.create_window(300, 160, window=browseButton_Excel)
 
button2 = tk.Button (root, text='2. GMM', command=getGMM, bg='SteelBlue1', font=('Helvetica', 11, 'bold'))
canvas1.create_window(300, 200, window=button2)

button3 = tk.Button (root, text='Kilépés', command=root.destroy, bg='SteelBlue1', fg='white', font=('Helvetica', 11, 'bold'))
canvas1.create_window(300, 280, window=button3)

button4 = tk.Button (root, text="3. Exportálás", command=export, bg='SteelBlue1', font=('Helvetica', 11, 'bold'))
canvas1.create_window(300, 240, window=button4) 

root.mainloop()