#df_creep = pd.read_csv("/Users/qbukold/Desktop/Schnulzen/creep_comments.tsv", sep='\t', lineterminator='\n')
#df_hurt = pd.read_csv("/Users/qbukold/Desktop/Schnulzen/hurt_comments.txt", sep="\t", lineterminator='\n')

import nltk 
nltk.download('words')
words = set(nltk.corpus.words.words())


def combine_strings(list, char):
    new_list = []
    temp_string = ""
    pos = 0
    try:
        for i, line in enumerate(list):
            if char in line:
                #
                if pos > 0:
                    new_list[pos] = new_list[pos] + " " + temp_string
                #
                pos = 0
                temp_string = ""
                new_list.append(line)
            else:
                pos = len(new_list) - 1
                temp_string = temp_string + " " + line


    except TypeError:
        pass
    return new_list

def append_if_english (creep):
    creep_new = []
    for line in creep:
        content = line.split("\t")
        author = content[0]
        comment = content[1]

        #tokenize comment
        tokens_com = nltk.wordpunct_tokenize(comment)
        print(tokens_com)

        #delete if no english words
        english = 0
        for token in tokens_com:
            if token.lower() in words:
                english += 1
            elif token.lower() in words and len(tokens_com) == 1:
                english += 100
        perc_en = english/len(tokens_com)

        if perc_en > 0.2:
            creep_new.append(line)
        return creep_new

#load tsv as list
creep = []
with open('/Users/qbukold/Desktop/Schnulzen/creep_comments.tsv', 'r') as content:
    for line in content.readlines():
        line = line.strip()
        if line != "":
            creep.append(line)
creep.pop(0)

## combine lines, if from same author
creep = combine_strings(creep, "\t")

## delete if not more than 20% english words OR one english Word
creep = append_if_english(creep)


with open("/Users/qbukold/Desktop/Schnulzen/creep_comments23.tsv", "w") as save_file:
    save_file.write("name\tcomment\n")
    for line in creep:
        if line.split("\t")[1] != "":
            save_file.write(line + "\n")
