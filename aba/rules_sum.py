import os
import time
import pandas as pd
import pickle 
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.tokenize import word_tokenize

#change the rule here
list_rules=["['s long']", "['lettre ramiste']", "['esperluette']", "['suppression lettre étymologique']", "['ajout accent aigu']", "['lettre calligraphique']", "['ajout accent circonflexe']", "['o → a imparfait/conditionnel']", "['es → é']", "['ajout accent grave']", "['tilde → voyelle + m/n']", "['transformation interne y  → i/ï']", 'unknown rule', "['fusion']", "['retrait tréma']", "['eu → u']", "['double consonne']", "['ct → t']", "['ajout d/t terminaison']", "['o → a sauf imparfait/conditionnel']", "['x/z → s']", "['terminaison y → is']", "['as → â']", "['cque/que → c']", "['retrait accent aigu']", "['cédille']", "['c → s']", "['apostrophe → e']", "['i → y']", "['gn → nn']", "['séparation']", "['ai/ei → e/è']", "['an/am ↔ en/em']", "['o ↔ au']", "['s → z']", "['retrait accent circonflexe']", "['s → t']", "['oing → oin']", "['s → c']", "['changement accent']", "['ph → f']", "['ajout h mot grec']", "['suppression l après voyelle']", "['ajout tréma']", "['t → d']", "['d → t']", "['séparation avec apostrophe']", "['retrait accent grave']", "['œ → e']", "['gd → d']", "['nt → mt']", "['voyelle + lt → voyelle + t']", "['erreur OCR']", "['æ → e']"]
#data_rule=list_rules[8]
#to store the results of number of occurrence for a rule
occurrences_df=[]

#create dir to store results
if os.path.isdir('sums') == False:
    os.mkdir("sums")

#create dir to store the graphs
if os.path.isdir('plots') == False:
    os.mkdir("plots")

#Get metadata file
meta_src=os.path.join('download','FreEMnorm','TableOfContent.tsv')
#Turn it into df
metadata = pd.read_table(
    meta_src,
    sep='\t',
    names = ['Author',
    'Title',
    'Date',
    'Place',
    'Word',
    'Line',
    'Genre',
    'Form',
    'Paratext',
    'BellesLettres',
    'Subcorpus',
    'Link',
    'File',
    'Wiki',
    'Image',
    'Sex',
    'Birth',
    'Deat',
    'BNF',
    'IdRef',
    'ISNI'])

#Get rule number
rule_number = 0

#loop over rules
for data_rule in list_rules:
    print("""
-----------------------------
          """)
    print(data_rule)
    print("""
-----------------------------
          """)
    time.sleep(1)

    #loop over files
    for file in os.listdir('rules'):
        #load file
        src=os.path.join('dicts',file)
        print(src)
        #make df
        df = pd.read_table(
            src,
            names = ['old',
            'new',
            'count',
            'chars_nb',
            'old_chars',
            'new_chars',
            'rules']
            )
        #Set counter to zero
        rules = {}
        i = 0
        totalCount = 0

        #get number of tokens
        file_content = open(os.path.join('download','FreEMnorm',"corpus",file)).read()
        #tokenize
        tokens = word_tokenize(file_content, language='french', preserve_line=True)
        #Get number of token
        tokens_number=len(tokens)
        #Divide by 2 (because src et trg)
        tokens_number_clean=int(tokens_number/2)
        #Print token number
        print("Tokens number: ", tokens_number_clean)

        #loop over the lines in the file to retrieve rules
        for line in df["rules"]:
            if line=="[]":
                line = "unknown rule"
            if line in rules.keys():
                rules[line] += df["count"][i]
            else:
                rules[line] = df["count"][i]
            totalCount += df["count"][i]   
            i += 1
        # order rules according to decreasing frequency
        rules = dict(sorted(rules.items(), key=lambda item: -item[1]))
        #save data as dict
        dict_file = '{}.{}'.format(file, '.pkl')
        with open(os.path.join('sums',dict_file), 'wb') as f:
            pickle.dump(rules, f)
        #get metadata row
        row = metadata[metadata['File'] == file]
        #get date in the row
        date=row.iloc[0, row.columns.get_loc('Date')]
        #count the occurrences of the rule if it exists
        if data_rule in rules:
            print("date:", date)
            print("Rule occurrences: ", rules[data_rule])
            normalize_data_rule=(int(rules[data_rule])/tokens_number_clean)*100
            occurrences_df.append({"Date": int(date), "Count":normalize_data_rule})
    #Make df out of the results of all the files
    new_df = pd.DataFrame(occurrences_df)
    #Sort data by date (increasing order)
    new_df = new_df.sort_values('Date')
    #Make a plot out of the data
    plt.figure(figsize=(10, 6))
    fig_occurrences=sns.lmplot(new_df, x="Date", y="Count", markers="+")
    #adding a title to the graph
    fig_occurrences.fig.suptitle(data_rule)
    #save image
    plt.savefig(os.path.join("plots",str(rule_number)), dpi=300)
    #Increment rule number
    rule_number += 1