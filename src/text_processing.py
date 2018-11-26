import re
import nltk
import numpy as np
import pickle



'''
    Json object containing mapping between contractions and extendend versions of verbs and others
    
    Key => Contracted form
    Value => Expanded form
'''
CONTRACTION_MAP = {"'s": "is", "ain't": "is not", "aren't": "are not","can't": "cannot", 
                   "can't've": "cannot have", "'cause": "because", "could've": "could have", 
                   "couldn't": "could not", "couldn't've": "could not have","didn't": "did not", 
                   "doesn't": "does not", "don't": "do not", "hadn't": "had not", 
                   "hadn't've": "had not have", "hasn't": "has not", "haven't": "have not", 
                   "he'd": "he would", "he'd've": "he would have", "he'll": "he will", 
                   "he'll've": "he he will have", "he's": "he is", "how'd": "how did", 
                   "how'd'y": "how do you", "how'll": "how will", "how's": "how is", 
                   "I'd": "I would", "I'd've": "I would have", "I'll": "I will", 
                   "I'll've": "I will have","I'm": "I am", "I've": "I have", 
                   "i'd": "i would", "i'd've": "i would have", "i'll": "i will", 
                   "i'll've": "i will have","i'm": "i am", "i've": "i have", 
                   "isn't": "is not", "it'd": "it would", "it'd've": "it would have", 
                   "it'll": "it will", "it'll've": "it will have","it's": "it is", 
                   "let's": "let us", "ma'am": "madam", "mayn't": "may not", 
                   "might've": "might have","mightn't": "might not","mightn't've": "might not have", 
                   "must've": "must have", "mustn't": "must not", "mustn't've": "must not have", 
                   "needn't": "need not", "needn't've": "need not have","o'clock": "of the clock", 
                   "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not",
                   "sha'n't": "shall not", "shan't've": "shall not have", "she'd": "she would", 
                   "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", 
                   "she's": "she is", "should've": "should have", "shouldn't": "should not", 
                   "shouldn't've": "should not have", "so've": "so have","so's": "so as", 
                   "this's": "this is",
                   "that'd": "that would", "that'd've": "that would have","that's": "that is", 
                   "there'd": "there would", "there'd've": "there would have","there's": "there is", 
                   "they'd": "they would", "they'd've": "they would have", "they'll": "they will", 
                   "they'll've": "they will have", "they're": "they are", "they've": "they have", 
                   "to've": "to have", "wanna": "want to", "wasn't": "was not", "we'd": "we would", 
                   "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", 
                   "we're": "we are", "we've": "we have", "weren't": "were not", 
                   "what'll": "what will", "what'll've": "what will have", "what're": "what are", 
                   "what's": "what is", "what've": "what have", "when's": "when is", 
                   "when've": "when have", "where'd": "where did", "where's": "where is", 
                   "where've": "where have", "who'll": "who will", "who'll've": "who will have", 
                   "who's": "who is", "who've": "who have", "why's": "why is", 
                   "why've": "why have", "will've": "will have", "won't": "will not", 
                   "won't've": "will not have", "would've": "would have", "wouldn't": "would not", 
                   "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would",
                   "y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have",
                   "you'd": "you would", "you'd've": "you would have", "you'll": "you will", 
                   "you'll've": "you will have", "you're": "you are", "you've": "you have" } 






'''
    Read data from file

    :param str filename: Name of the local file to be opened
'''
def load_doc(filename):

    file = open(filename, 'r')
    text = file.read()
    file.close()
    
    return text


'''
    TO DO DESCRIPTION
'''
def expand_contractions(sentence, contraction_mapping):
    
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_sentence = contractions_pattern.sub(expand_match, sentence)
    return expanded_sentence


'''
    TO DO DESCRIPTION
'''
def preprocess_sentence(sentence):
    # Transform some punctuation to space
    line = re.sub(r"[,.;@#?!]+\ *", " ", sentence)
    
    # Remove contractions
    line = expand_contractions(line, CONTRACTION_MAP)

    # Convert to lower case
    line = line.lower()

    # Tokenize words
    default_wt = nltk.word_tokenize
    line = default_wt(line)
    
    # Remove contractions in tokens
    line = [CONTRACTION_MAP[i] if i in CONTRACTION_MAP else i for i in line]
    
    return line


'''
    TO DO DESCRIPTION
'''
def prepare_data(data):
    
    english_sentences, german_sentences = [], []
    
    set_english = set()
    
    i = 0
    # Read line by line
    for line in data.split("\n"):
        
        # Split line into English and German parts
        line_split = line.split("\t")
        
        # Assert that there are two translations
        assert(len(line_split) == 2)
        
        # Normalization and tokenization
        line_english, line_german = preprocess_sentence(line_split[0]), preprocess_sentence(line_split[1])
        
        # I do not want duplicates of sentences in English
        tmp_eng = " ".join(line_english)
        if tmp_eng not in set_english:
            set_english.add(tmp_eng)
            
            # Add new row to all sentence in the two languages
            english_sentences.append(line_english)
            german_sentences.append(line_german)
            
            i+=1
            
        #debug    
        if i >=55000: break        

    return np.array(english_sentences), np.array(german_sentences) 


'''
    TO DO DESCRIPTION
'''
def max_length_sentence(dataset):
    return max([len(line) for line in dataset])


'''
    TO DO DESCRIPTION
'''
def pad_sentence(tokenized_sentence, max_length_sentence, padding_value=0, pad_before=True):
    
    pad_length = max_length_sentence - len(tokenized_sentence)
    sentence = list(tokenized_sentence)
    
    if pad_length > 0:
        if pad_before:
            return np.pad(tokenized_sentence, (pad_length, 0), mode='constant', constant_values=int(padding_value))
        else:
            return np.pad(tokenized_sentence, (0, pad_length), mode='constant', constant_values=int(padding_value))
    else: # Cut sequence if longer than max_length_sentence
        return sentence[:max_length_sentence]

    
'''
    TO DO DESCRIPTION AND COMMENTS!!!
'''   
def prepare_sequences(source_sentences, target_sentences, source_dict, target_dict):
    
    source_input, target_input = [], []
    
    for i in range(len(source_sentences)):
        
        # Prepare source sentence
        source = list(source_sentences[i])
        source_mapped = source_dict.text_to_indices(source)
        padded_source = pad_sentence(source_mapped, source_dict.max_length_sentence)
        
        # Prepare target sentence
        target = list(target_sentences[i])
        target.insert(0, "<START>")
        target.append("<END>")
        target_mapped = target_dict.text_to_indices(target)
        padded_target = pad_sentence(target_mapped, target_dict.max_length_sentence, pad_before=False)
        
        # Append sentences
        source_input.append(padded_source)
        target_input.append(padded_target)

    return np.array(source_input), np.array(target_input)
    

'''
    TO DO DESCRIPTION
'''      
def load_dump(filename):
    return pickle.load(open(filename, "rb" ))


'''
    TO DO DESCRIPTION
'''   
def save_dump(object_to_save, filename):
    pickle.dump(object_to_save, open(filename, "wb"))
    