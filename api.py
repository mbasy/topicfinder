from datetime import datetime
start_time = datetime.now()
import pandas as pd
import re
import sys
import platform 
import argparse
from distutils.log import debug
from fileinput import filename
from flask import *  
app = Flask(__name__)  

def get_topic(file1, file2)->list:
    cat_file = pd.ExcelFile(file1)
    sheet_to_df_map = {}
    for sheet_name in cat_file.sheet_names:
        sheet_to_df_map[sheet_name] = cat_file.parse(sheet_name)

    my_series = pd.Series(sheet_to_df_map)

    cat_file = my_series[my_series.notna()].to_dict()
    #cat_file = cat_file.apply(lambda s: s.dropna().astype(str).tolist()).to_dict()
    text_file = pd.read_excel(file2)
    text_file = text_file['Ärende'].to_list()

    def get_dict_key(dictionary)->list:
        return list(dictionary.keys())

    cat_list = get_dict_key(cat_file)
    #print(cat_list)


    index_counter = 0

    parser = argparse.ArgumentParser(description="Script")
    parser.add_argument("--text")
    args, leftovers = parser.parse_known_args()

    print("Arg has been set (value is {0})".format(args.text))
    s_text = text_file
    print('\n')

    word_counter = 0

    cat_result = []
    result_list = []
    for n_of_text in s_text:
        print("Reading text:",word_counter+1)
        for t in cat_list:
            r = re.findall(r'|'.join(cat_file[t]), n_of_text, re.IGNORECASE)
            if(r):
            # print(f"{bcolors.OKCYAN}Topic found(",t,"):",r, bcolors.ENDC)
                if(t in cat_result):
                    result_list[cat_result.index(t)] = result_list[cat_result.index(t)]+len(r)
                else:
                    cat_result.append(t)
                    result_list.append(len(r))
                    #print("\t","Number of words found:", word_counter, "Total words in text file:", number_of_word_in_text,
                # round((word_counter/number_of_word_in_text)*100, 2), "%")
        word_counter += 1

    print(cat_result)
    print(result_list)
    html_list = []
    loop_counter = 0
    total_value = sum(result_list)
    for cat in cat_result:
        #print(f"Topic found(",cat_result[loop_counter],"):"
        #    , result_list[loop_counter],"Total:", round((result_list[loop_counter]/total_value)*100, 2), "%")
        dt = f"{cat_result[loop_counter]} {round((result_list[loop_counter]/total_value)*100, 2)}%"
        html_list.append(dt)
        loop_counter+=1
    return(html_list)

def print_ul(elements):
    print("<ul>")
    for s in elements:
        ul = "<li>" + str(s) + "</li>"
        print(ul)
    print("</ul>")

@app.route('/')  
def main():  
    return render_template("index.html")  
  
@app.route('/success', methods = ['POST'])  

def success(): 
    if request.method == 'POST':  
        f1 = request.files['file1']
        f2 = request.files['file2']
        f1.save(f1.filename)
        f2.save(f2.filename)
        return render_template("Acknowledgement.html", name1 = f1.filename, name2 = f2.filename,
                               result = get_topic(f1.filename, f2.filename))  
if __name__ == '__main__':  
    app.run(host="0.0.0.0")