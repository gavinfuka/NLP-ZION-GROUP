import pandas as pd
import numpy as np


# remove redundancy word and make it can be open by pandas
def modify_data(file):
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.replace(';Work', '\tWork')
            line = line.replace('Author: ', '')
            line = line.replace('Work Time(s): ', '')
            file_data += line
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)


# get all answer of the question
def get_answer(file):
    output_list = pd.read_csv(file, sep='	', header=None)
    return output_list

# separate each 4 question to 4 columns
def separate_question(input_list):
    output_list = []
    if input_list[0].find('one:') != -1:
        output_list.append(input_list[0][0:3])
        output_list.append(input_list[0][5:])
    elif input_list[0].find('multiple:') != -1:
        output_list.append(input_list[0][0:8])
        output_list.append(input_list[0][10:])
    # print(input_list[1:])
    output_list.extend(input_list[1:])
    return output_list


def transfer(data_file, answer_file):
    modify_data(data_file)
    data = pd.read_csv(data_file, sep='\t', header=None)
    answer_data = get_answer(answer_file)
    df_new = pd.DataFrame()
    for index, row in data.iterrows():
        new_columns = row[0:4].values
        for i in range(4):
            # print(row[4 + 5 * i: 4 + 5 * i + 5].values)
            temp_list = separate_question(row[4 + 5 * i: 4 + 5 * i + 5].values)
            final_columns = np.append(new_columns, temp_list)
            final_columns = np.append(final_columns, answer_data[i][index])
            final_columns = final_columns.tolist()
            df_new = df_new.append([final_columns], ignore_index=True)
    df_new.columns = ['id', 'author', 'work_times', 'article', 'question_type', 'question', 'A', 'B', 'C', 'D',
                      'answer']
    return df_new


def main():
    data_dict = {'mc160.train': '../data/MCTest/MCTest/mc160.train.tsv',
                 'mc160.dev': '../data/MCTest/MCTest/mc160.dev.tsv',
                 'mc160.test': '../data/MCTest/MCTest/mc160.test.tsv',
                 'mc500.train': '../data/MCTest/MCTest/mc500.train.tsv',
                 'mc500.dev': '../data/MCTest/MCTest/mc500.dev.tsv',
                 'mc500.test': '../data/MCTest/MCTest/mc500.test.tsv', }
    answer_dict = {'mc160.train': '../data/MCTest/MCTest/mc160.train.ans',
                   'mc160.dev': '../data/MCTest/MCTest/mc160.dev.ans',
                   'mc160.test': '../data/MCTest/MCTestAnswers/mc160.test.ans',
                   'mc500.train': '../data/MCTest/MCTest/mc500.train.ans',
                   'mc500.dev': '../data/MCTest/MCTest/mc500.dev.ans',
                   'mc500.test': '../data/MCTest/MCTestAnswers/mc500.test.ans', }
    for key in data_dict:
        df = transfer(data_file=data_dict[key], answer_file=answer_dict[key])
        df.to_csv('../std_data/MCTest/'+key[0:5]+'/'+key+'.csv')
main()
