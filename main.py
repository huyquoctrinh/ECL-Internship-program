import csv 
import numpy as np 
from tqdm import tqdm
import json
from utils import save_np
import os

'''

This is the function for extract csv file to np array data.

Input:

- csv_input (str): filename of file csv
- txt_path (str): file path of file txt event
- dst (str): file to save
- no_src (int): how much items you want to save. For ex: len(plus1 + essel) = 2 items
'''

def extract_csv(csv_input, txt_path, dst, no_src = 2):
    
    # txt_path = "./Memory_Trinh/A02/4letter/event.txt"
    f = open(txt_path, "r")

    lines = f.readlines()
            
    file = open(csv_input)
    csv_reader = csv.reader(file)
    # print(csv_reader)
    # dst = "./Memory_extracted/"
    i = 0
    data = []
    labels = []
    res = dict()
    lb_tmp = ''
    cnt = 0
    ck = 1

    for row in csv_reader:
        # try:
        # print(row)
            i+=1
            if (i>26):
                if row[2] == 'StartMedia':
                    # labels.append(row[6])
                    # print(row[6])
                    pass
                    # lb_tmp = row[6]
                if row[2] == '':
                    # print(type(row[8:-1]))
                    data.extend(list(map(float,row[8:-1])))
                if row[2] == 'EndMedia':
                    if ck%2==0 and ck%4 != 0:
                        lb_tmp = row[6]
                        data = np.array(data)
                        # print(lines[i])
                        lb_folder = lines[27+cnt].split("  ")[0].split("\t")[2]
                        # print(lb_folder)
                        # print(lines[26+cnt+1].split("  ")[0].split("\t")[2])
                        if lb_folder == "63":
                            # print("case")
                            num_r = lines[27+cnt+1].split("  ")[0].split("\t")[2]
                            if num_r == "1" or num_r == "2":
                                save_np(dst + "/" + lb_folder + str(num_r) +"/"+str(lb_tmp)+".npy", data)
                        if lb_folder == "62":
                            # if num_r != 1 or num_r != 2:
                            #     pass
                            num_r = lines[27+cnt+1].split("  ")[0].split("\t")[2]
                            # print(lb_folder + num_r)
                            if num_r == "1":
                                num_r2 = lines[27+cnt+2].split("  ")[0].split("\t")[2]
                                print(dst + "/" + lb_folder + str(num_r) +str(num_r2) +"/"+str(lb_tmp)+".npy")
                                save_np(dst + "/" + lb_folder + str(num_r) +str(num_r2) +"/"+str(lb_tmp)+".npy", data)
                            else:
                                # print("case")
                                # if num_r == "1" or num_r == "2":
                                save_np(dst + "/" + lb_folder + str(num_r) +"/"+str(lb_tmp)+".npy", data)
                    # save_np(dst + "/"+str(lb_folder)+str(cnt)+ "/"+str(lb_tmp) + ".npy", data)
                        cnt+=4
                        ck += 1
                        data = []
                        lb_tmp = ''
                    else:
                        ck+=1
                        continue

'''

This is the function to extract data from full source:

    src (str): folder that contain data in format:
    <Folder name>: 
    + Number_ID 1:
        + Letter ID 1:
            + <name>.csv
            + event.txt
        ...
    ...

    dst (str): the output folder, follow this format

    <Folder name>
    + Label name 1:
        + Data sample 1
        ...
    ...

'''

def extract_full(src, dst):
    list_id = os.listdir(src)    
    list_lb = ["6211", "631", "632","6212","622","6288"]
    for lb in list_lb:
        os.mkdir(os.path.join(dst, lb))

    for id in list_id:
        letters_src =os.path.join(src, id)
        letters = os.listdir(letters_src)
        for letter in letters:
            
            extract_src = os.path.join(letters_src, letter)
            csv_file, event_file = os.listdir(extract_src)
                # print(csv_file, event_file)
            try:
                extract_csv(extract_src + "/"+csv_file, extract_src + "/"+event_file, dst)
            except:
                continue
    
src = "./Memory_Trinh/"
dst = "./final_data/"
extract_full(src, dst)
