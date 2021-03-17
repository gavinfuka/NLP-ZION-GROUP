import json
import pandas as pd
import os
def json2dict(file):
    with open(file,"r") as f:
        load_dict = json.load(f)
    return load_dict


def transfer(file,df_new):

    temp_dict=json2dict(file)
    fix_column=[temp_dict['id'],temp_dict['article']]
    for i in range(len(temp_dict['questions'])):
        final_columns=[]
        final_columns.extend(fix_column)
        final_columns.append(temp_dict['questions'][i])
        for j in range(len(temp_dict['options'][i])):
            final_columns.append(temp_dict['options'][i][j])
        final_columns.append(temp_dict['answers'][i])
        if (temp_dict['answers'][i] not in ['A','B','C','D']):
            print('?')
        df_new = df_new.append([final_columns], ignore_index=True)
    return df_new

#得到文件夹下的所有文件名称
def get_file_name(path):
    files = os.listdir(path)
    return files
def main():
    type_list=['dev','train','test']
    school_list=['high','middle']

    for type in type_list:
        for school in school_list:
            df_new = pd.DataFrame()
            path = '../data/RACE/RACE/'+type+'/'+school+'/'
            files=get_file_name(path)
            for file in files:
                df_new=transfer(path+file,df_new)
            df_new.columns = ['id', 'article','question', 'A', 'B', 'C', 'D',
                              'answer']
            df_new.to_csv('../std_data/RACE/' + school + '/' + type + '.csv')


main()