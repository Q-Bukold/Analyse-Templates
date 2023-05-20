import nltk 

#df_creep = pd.read_csv("/Users/qbukold/Desktop/Schnulzen/1000_creep.tsv", sep='\t', lineterminator='\n')
#df_hurt = pd.read_csv("/Users/qbukold/Desktop/Schnulzen/1000_hurt.tsv", sep="\t", lineterminator='\n')
#df_abba = pd.read_csv("/Users/qbukold/Desktop/Schnulzen/1000_abba.tsv", sep="\t", lineterminator='\n')
#df_gwtw = pd.read_csv("/Users/qbukold/Desktop/Schnulzen/600_gwtw.tsv", sep="\t", lineterminator='\n')

def append_if_english(list, origin):
    list_new = []
    for line in list:
        content = line.split("\t")
        id = content[0]
        author = content[1]
        comment = content[2]

        line = line + "\t" + origin

        #tokenize comment
        tokens_com = nltk.wordpunct_tokenize(comment)

        #delete if no english words
        english = 0
        non_english = len(tokens_com)
        my_exceptions = ["el", "mi", "de", "viva", "sin", "y", "es", "las", "ne", "l", "la", "se", "lo", "hasta", "fin", "no"]
        for token in tokens_com:
            if token.lower() in words and token.lower() not in my_exceptions:
                english += 1
            elif token.lower() in words and len(tokens_com) == 1:
                english += 100
            elif token == " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~":
                non_english -= 1

        perc_en = english/non_english
        if perc_en > 0.25:
            list_new.append(line)
            
    return list_new

def load_tsv_list(filename):
    list = []
    with open(filename, 'r') as content:
        for i, line in enumerate(content.readlines()):

            if i == 0:
                continue #skip first line
            
            try:
                line = line.strip()
                content = line.split("\t")
                id = content[0]
                author = content[1]
                comment = content[2]
                list.append(line)
            except IndexError:
                continue
            except Exception as e:
                print(e)
    return list


#nltk.download('words')
words = set(nltk.corpus.words.words())

#load tsv as list
creep = load_tsv_list("/Users/qbukold/Desktop/Schnulzen/1000_creep.tsv")
hurt = load_tsv_list("/Users/qbukold/Desktop/Schnulzen/1000_hurt.tsv")
abba = load_tsv_list("/Users/qbukold/Desktop/Schnulzen/1000_abba.tsv")
gwtw = load_tsv_list("/Users/qbukold/Desktop/Schnulzen/600_gwtw.tsv")

## delete if not more than 20% english words OR one english Word and add Origin-Column
creep_new = append_if_english(creep, "Creep")
hurt_new = append_if_english(hurt, "Hurt")
abba_new = append_if_english(abba, "The Winner Takes It All")
gwtw_new = append_if_english(gwtw, "Tara's Theme")

print("creep_new", len(creep_new))
print("hurt_new", len(hurt_new))
print("abba_new", len(abba_new))
print("crgwtw_neweep", len(gwtw_new))


all_new = creep_new + hurt_new + abba_new + gwtw_new
all_new.insert(0, "old_id\tauthor\tcomment\torigin")

all_200per = creep_new[:200] + hurt_new[:200] + abba_new[:200] + gwtw_new[:200]
all_200per.insert(0, "old_id\tauthor\tcomment\torigin\tcategory")



with open("/Users/qbukold/Desktop/Schnulzen/all_annotate_800.tsv", "w") as save_file:
    for line in all_200per:
        if line.split("\t")[1] != "":
            save_file.write(line + "\n")


