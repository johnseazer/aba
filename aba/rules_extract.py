import glob, os, re, subprocess
import pandas as pd
from shutil import copyfile

# Pour lancer ce script :
# python -m aba.rules_extract

# Auparavant, mettre le corpus (fichiers TSV) à traiter dans le dossier corpus (frère du dossier aba)
# Ces fichiers TSV peuvent contenir 2 colonnes ou plus
# (1e : normalisée ; 2e : originale ; si inverse remplacer 
#           outputFile.writelines(res.group(2)+"\t"+res.group(1)+"\n")
# par 
#           outputFile.writelines(res.group(1)+"\t"+res.group(2)+"\n")
# )

firstTime = True
#firstTime = False

download_folder = os.path.join(os.path.join('download','FreEMnorm'),'corpus')

def empty_download_folder(download_folder):
    # Empty download folder
    download_folder_files = glob.glob(os.path.join(download_folder,'*'))
    for f in download_folder_files:
        ## print("Removing file " + f + " from download folder")
        os.remove(f)

# Copying source files from the corpus folder
corpus_folder = os.path.join('corpus','*.tsv')

print(corpus_folder)
files = glob.glob(corpus_folder)

"""
files = [
'splitByYear-LowerThan1630.tsv',
'splitByYear-LowerThan1660.tsv',
'splitByYear-LowerThan1670.tsv',
'splitByYear-LowerThan1680.tsv',
'splitByYear-LowerThan1700.tsv'
]
"""
ruleTable = {}

fileNb = 0

bigRuleFile = open('dic_p17_labeled.tsv','w',encoding='utf-8')

fileSize = {}


##print("Starting to copy files")
for f in files:
    #f = os.path.join("corpus", f)
    empty_download_folder(download_folder)
    
    filename = os.path.basename(f)
    print(filename)
    ##print("Copying file " + filename + " to download folder")
    ##print("New file:" + os.path.join(download_folder, filename))
    #copyfile(f, os.path.join(download_folder, filename))
    

    outputFile = open(os.path.join(download_folder, filename), "w", encoding="utf-8")
    for line in open(f, "r", encoding="utf-8"):
       #res = re.search("^([^\t]*)\t([^\t]*)\t.*$", line)
       res = re.search("^([^\t]*)\t([^\t\r\n]*)[\r\n]*$", line)
       if res:
          #outputFile.writelines(res.group(2)+"\t"+res.group(1)+"\n")
          outputFile.writelines(res.group(1)+"\t"+res.group(2)+"\n")
    outputFile.close()
    
    # empty word alignment folder
    word_alignment_folder = os.path.join('data','FreEMnorm_words')
    word_alignment_files = glob.glob(os.path.join(word_alignment_folder,'*'))
    
    for f in word_alignment_files:
        print("Removing file " + f + " from word alignment folder")
        os.remove(f)
    
    if firstTime:
       # call align_words and save file if it is the first time the script is called on those files
       subprocess.call("python -m aba.align_words")
       copyfile(os.path.join(os.path.join('data','FreEMnorm_words'),filename), os.path.join(os.path.join('corpus','FreEMnorm_words'),filename))
    else:
       # load the file otherwise
       copyfile(os.path.join(os.path.join('corpus','FreEMnorm_words'),filename), os.path.join(os.path.join('data','FreEMnorm_words'),filename))

    # save number of Words
    wordFile = open(os.path.join(os.path.join('data','FreEMnorm_words'),filename), "r", encoding="utf-8")
    fileSize[filename] = 0
    for line in wordFile:
       fileSize[filename] += 1
    wordFile.close()

    # find rules
    subprocess.call("python -m aba.analyze")

    # save rules
    ruleFile = open(os.path.join('data','dic_p17_labeled.tsv'),'r',encoding='utf-8')
    for line in ruleFile:
       bigRuleFile.writelines(filename + "\t" + line)
    ruleFile.close()

    src = os.path.join('data','dic_p17_labeled.tsv')

    df = pd.read_table(
		    src,
        names = ['old',
                 'new',
                 'count',
                 'chars_nb',
                 'old_chars',
                 'new_chars',
                 'rules'])

    i = 0
    totalCount = 0
    rules = {}
    
    for line in df["rules"]:
        if line=="[]":
            line = "règle inconnue"
        if line in rules.keys():
            rules[line] += df["count"][i]
        else:
            rules[line] = df["count"][i]
        totalCount += df["count"][i]
        i += 1
        
    ##print(rules)
    
    for r in rules.keys():
        ##print(r)
        ##print("a")
        ruleInTexts = []
        if r in ruleTable.keys():
            ruleInTexts = ruleTable[r]
            i = len(ruleInTexts)
            while i < fileNb:
                ruleInTexts.append(0)
                i += 1    
        else:
            i = 0
            while i < fileNb:
                ruleInTexts.append(0)
                i += 1    
        ruleInTexts.append(rules[r])
        ruleTable[r] = ruleInTexts
    
    ##print("Rules after text " + str(i) + ":")    
    ##print(ruleTable)

    fileNb += 1
    ##print(ruleTable.keys())
    ##print(str(fileNb)+ "=?" +str(len(ruleTable[list(ruleTable.keys())[0]])))


fileNb = 0

output = open("output-rule.tsv","w",encoding="utf-8")
outputR = open("output-rule-r.txt","w",encoding="utf-8")

output.writelines((";".join(list(ruleTable.keys()))).replace("'","")+"\n")
matrix = ""
i=0
for f in files:
    newLine = ""
    for j in range(0, len(list(ruleTable.keys()))):
        i += 1
        if fileNb < len(ruleTable[list(ruleTable.keys())[j]]):
           value = str(ruleTable[list(ruleTable.keys())[j]][fileNb]/fileSize[os.path.basename(f)]) 
           
        else:
           value = "0"
        newLine += value + ";"
        if i==1:
            matrix += value
        else:
            matrix += ","+value
    fileNb += 1
    output.writelines(newLine+"\n")
    #print(fileSize[os.path.basename(f)])
    
    
output.close()

shorterFiles = []
for f in files:
   res = re.search("corpus.([^_]+_[^_]+)_.*",f)
   if res:
      shorterFiles.append(res.group(1))
   else:
      res = re.search("corpus.(.*).tsv",f)
      if res: 
         shorterFiles.append(res.group(1))

outputR.writelines("https://rdrr.io/snippets/\n")
outputR.writelines("library(FactoMineR)\n")
outputR.writelines("library(factoextra)\n")
outputR.writelines("tab <- matrix(c(" + matrix + "), ncol=" + str(len(list(ruleTable.keys()))) + ", byrow=TRUE)\n")
outputR.writelines("colnames(tab) <- c('" + "','".join(list(ruleTable.keys())).replace("'","").replace(",","','") + "')\n")
outputR.writelines("rownames(tab) <- c('" + "','".join(shorterFiles) +"')\n")
outputR.writelines("\n")
outputR.writelines("tab <- as.table(tab)\n")
outputR.writelines("\n")
outputR.writelines("class(tab) <- \"numeric\"\n")
outputR.writelines("aX <- as.data.frame(tab)\n")
outputR.writelines("\n")
outputR.writelines("aX\n")
outputR.writelines("res.pca = PCA(aX, scale.unit=TRUE, ncp=2, graph=T)\n")
outputR.writelines("\n")
outputR.writelines("ind <- get_pca_ind(res.pca)\n")
outputR.writelines("ind$coord\n")
outputR.writelines("var <- get_pca_var(res.pca)\n")
outputR.writelines("var$coord")
outputR.close()