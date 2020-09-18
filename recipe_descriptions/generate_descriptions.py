def gen_sent_1(word, start):
    token = word
    sent = [word]

    # loop repeatedly
    while True:
        try:
            # randomly select a probable next token
            token = choice(start[sent[-1]]['token'], p=start[token]['prob'])

            sent.append(token)
        except KeyError:
            # there is no next token to select! exit the loop
            break
    return ' '.join(sent[:-1]).capitalize()+sent[-1]
    
def gen_sent_2(word, start, overall):
    token = word
    sent = [word]

    # loop repeatedly
    while True:
        try:
            # randomly select a probable next token
            if len(sent)==1:
                # use the first-2 dictionary to select second token
                token = choice(start[sent[-1]]['token'], p=start[token]['prob'])
            else:
                # select next token based on previous 2
                token = choice(overall[' '.join(sent[-2:])]['token'], p=overall[' '.join(sent[-2:])]['prob'])

            sent.append(token)
        except KeyError:
            # there is no next token to select so exit the loop
            break
    return ' '.join(sent[:-1]).capitalize()+sent[-1]