from sys import argv

def generate_sentences(data_structs, m):
    from numpy.random import choice
    from re import sub

    word = choice(data_structs[0].index, p=data_structs[0].values)
    sent = [word]
    
    i = 1
    while True:
        try:
            token = ' '.join(sent[-m:]).replace(' ,', ',')
            next_word = choice(data_structs[min(i, m)][token]['token'], p=data_structs[min(i, m)][token]['prob'])

            sent.append(next_word)
            i += 1
        except KeyError:
            # no next token, exit loop
            break

    # join words into complete sentence
    return sub(r"\s(?=[^\w])", '', ' '.join(sent)).capitalize()
    
def make_dictionaries(file_dir, m=2):
    from re import sub, findall
    from nltk import sent_tokenize
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.text import CountVectorizer
    
    # read in input file
    try:
        with open(file_dir, 'r') as f:
            text = f.read()
    except:
        print("Unable to open input .txt file. Rerun with correct path to input .txt.")
        return

    # ---------------- data cleaning -----------------
    # split into sentences (one per item in series)
    df = pd.Series(sent_tokenize(text))
    del text
    
    # lowercase everything
    df = df.str.lower()
    
    # remove stray apostrophes and parenthesis
    df = df.apply(lambda x:sub(r"((?<=\s)'|'(?!\w))", '', x))
    df = df.apply(lambda x:sub('\"', '', x))
    df = df.apply(lambda x:sub(r"[\(\)\[\]]", '', x))
    df = df.apply(lambda x:sub(r"(?<=[a-zA-Z]),", ' commaplaceholder ', x))
    
    def sub_endline(x):
        endline = findall(r"\W*$", x)[0]

        if '\!' in endline:
            return sub(r"\W*$", ' eendline', x)
        elif '\?' in endline:
            return sub(r"\W*$", ' qendline', x)
        else:
            return sub(r"\W*$", ' pendline', x)

    df = df.apply(sub_endline)
    
    # ---------- create data structures ------------------
    data_structs = [None] * (m+1)
    
    # probabilities for the starting word
    data_structs[0] = df.str.split(n=1).str[0].value_counts()
    data_structs[0] = data_structs[0] / data_structs[0].sum()
    
    # distributions for subsequent words
    for i in range(1, m+1):
        vect = CountVectorizer(token_pattern=r"(?u)\b[^\s]+\b", analyzer='word',
                               ngram_range=(i+1,i+1))
        vect.fit(df)

        # get occurrences out of vect
        pairs = pd.Series(np.asarray(vect.transform(df).sum(axis=0)).reshape(-1),
                  index=vect.get_feature_names(), name='freq')

        pairs.index.name = 'tokens'
        pairs = pairs.reset_index()

        # expand to 2 columns (prompt, response)
        pairs = pd.concat([pairs['tokens'].str.rsplit(n=1, expand=True).rename(columns={0:'prompt', 1:'response'}),
                  pairs['freq']], axis=1)

        # undo endline/comma substitutions
        pairs['prompt'] = pairs['prompt'].apply(lambda x:sub(r"\s*commaplaceholder", ',', x))
        pairs['response'] = pairs['response'].apply(lambda x:sub(r"\s*commaplaceholder", ',', x)).replace('pendline', '.').replace('qendline', '?').replace('eendline', '!')

        # store results in a dictionary
        doubles = {}
        for token, group in pairs.groupby('prompt'):
            doubles[token] = {'prob':(group['freq']/group['freq'].sum()).values,
                             'token':group['response'].values}
            
        data_structs[i] = doubles
            
    # export data
    import pickle

    with open('data.pkl', 'wb') as f:
        pickle.dump(data_structs, f)
    f.close()
    
def main():
    import argparse, os, pickle

    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', help="Path to raw .txt file. If none is provided, defaults to most recently-created dictionaries.", type=str)
    parser.add_argument('--simulations', '-s', help="the # of random sentences to build, defaults to 10", type=int, default=10)
    parser.add_argument('--markovsize', '-m', help="the # of tokens to consider when building sentences, defaults to 2", type=int, default=2)
    parser.add_argument('--randomseed', '-r', help="the random seed to use when building sentences, defaults to 1", type=int, default=1)
    args = parser.parse_args()
    
    if args.filename is None:
        # check if there's already a data file to read
        try:
            # attempt to read data and make sure it's large enough
            with open('data.pkl', 'rb') as f:
                data_structs = pickle.load(f) 
            f.close()
            
            assert args.markovsize<=len(data_structs)-1
            
        except AssertionError:
            print("ERROR: Data file exists but isn't large enough.\nPlease re-run with the -f filename argument, and appropriately large -m markovsize argument")
            return
        except:
            print("ERROR: No existing data file.\nPlease rerun with the -f filename argument.")
            return
    else:
        # no data file, so create one
        print("- Building new dictionaries.\n")
        make_dictionaries(args.filename, m=args.markovsize)
            
    
    # import data file
    with open('data.pkl', 'rb') as f:
        data_structs = pickle.load(f)
    f.close()
    
    # generate random sentences
    print("Generating {} sentences:\n".format(args.simulations))
    from numpy.random import choice, seed
    seed(args.randomseed)
        
    for i in range(args.simulations):
        print(generate_sentences(data_structs, args.markovsize))
    
if __name__ == '__main__':
    main()