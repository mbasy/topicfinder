from datetime import datetime
start_time = datetime.now()
import pandas as pd
import re
import os
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
    text_file = pd.read_excel(file2)
    text_file = text_file['Ärende'].to_list()

    def get_dict_key(dictionary)->list:
        return list(dictionary.keys())

    cat_list = get_dict_key(cat_file)

    s_text = text_file

    os.remove(file1)
    os.remove(file2) 
	
    word_counter = 0

    cat_result = []
    result_list = []
    for n_of_text in s_text:
        for t in cat_list:
            r = re.findall(r'|'.join(cat_file[t]), n_of_text, re.IGNORECASE)
            if(r):
                if(t in cat_result):
                    result_list[cat_result.index(t)] = result_list[cat_result.index(t)]+len(r)
                else:
                    cat_result.append(t)
                    result_list.append(len(r))
        word_counter += 1
    html_list = []
    loop_counter = 0
    total_value = sum(result_list)
    for cat in cat_result:
        dt = f"{cat_result[loop_counter]} : {round((result_list[loop_counter]/total_value)*100, 2)}%"
        html_list.append(dt)
        loop_counter+=1
    return(html_list)

@app.route('/')  
def main():  
    return render_template("index.html")  
  
@app.route('/topic_api', methods = ['POST'])  

def success(): 
    if request.method == 'POST':  
        f1 = request.files['file1']
        f2 = request.files['file2']
        f1.save(f1.filename)
        f2.save(f2.filename)
        return render_template("Acknowledgement.html", name1 = f1.filename, name2 = f2.filename,
                               result = get_topic(f1.filename, f2.filename))  

@app.route('/topic_api_json', methods = ['POST']) 

def api_only():
    if request.method == 'POST':  
        f1 = request.files['file1']
        f2 = request.files['file2']
        f1.save(f1.filename)
        f2.save(f2.filename)
        result = get_topic(f1.filename, f2.filename)
        return result

if __name__ == '__main__':  
    app.run(host="0.0.0.0")