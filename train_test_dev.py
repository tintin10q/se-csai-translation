import os
import codecs
import argparse
import errno
import logging
from sklearn.model_selection import train_test_split
from sacremoses import MosesTokenizer
from joblib import Parallel, delayed

class SmallerSizeError(Exception):
    """Exception raised for errors in the length of input data compared to the split size. """
    def __init__(self, message="Not enough data to split"):
        self.message = message
        super().__init__(self.message)
        
def split_ttd(srcF, trgF, size):
    """ Splits a source and a target files into 
        train test and dev sets retaining sentence alignment 
        
        :param srcF: the soure-language file (string/path)
        :param trgF: the target-language file (string/path)
        :param size: the size for the test and dev sets (int)
        :return: source and target splits (dictionaries)
    """  
    if not os.path.exists(srcF):
        logging.error("Source file does not exist")
        raise FileNotFoundError()
    if not os.path.exists(trgF):
        logging.error("Target file does not exist")
        raise FileNotFoundError()
    
    with codecs.open(srcF, 'r', 'utf8') as srcFile, codecs.open(trgF, 'r', 'utf8') as trgFile:
        src_data = srcFile.readlines()
        trg_data = trgFile.readlines()

    src = {}
    trg = {}

    # if there is not enough data to be split there we abort
    if len(src_data) <= 2 * size and len(trg_data) <= 2 * size:
        logging.error("Not enough data to split")
        raise SmallerSizeError()
        
    src['train'], src['test'], trg['train'], trg['test'] = train_test_split(src_data, trg_data, shuffle=True, test_size=size*2, random_state=42)
    src['dev'], src['test'], trg['dev'], trg['test'] = train_test_split(src['test'], trg['test'], shuffle=True, test_size=size, random_state=42)

    return src, trg
    
def tokenize(text_dict, lang):
    """ Tokenizes the text using Moses tokenizer.
    
        :param text_dict: A dictionary containing the three splits of text (dictionary)
        :param lang: The language of the text (string)
        :return: a dictionary with tokenized text for each of the splits (dictionary)
    """  

    mt =  MosesTokenizer(lang=lang)

    tokenized_text_dict = {}
    for split in text_dict:
        # The following line will run the tokenization on a single thread
        tokenized_text_dict[split] = [mt.tokenize(sent.rstrip(), return_str=True, escape=False) for sent in text_dict[split]]
        # The following line will run the tokenization in parallel (uncomment it if you want to use it and comment the above line)
        # tokenized_text_dict[split] = Parallel(n_jobs=-1)(delayed(mt.tokenize)(sent.rstrip(), return_str=True, escape=False) for sent in text_dict[split])

    return tokenized_text_dict

def clean(src_tok, trg_tok, cutoff):
    """ Cleans the source and target text together. 
        That is, removes sentences from the source and 
        the target side with a joint length of more than 
        the specified cut-off length
    
        :param src_tok: tokenized source data (list of string)
        :param trg_tok: tokenized target data (list of string)
        :param cutoff: the cut-off length (int)
        :return: cleaned source and target data  
    """
    
    # now let's clean the training data
    src_trg_clean = [(s, t) for s, t in zip(src_tok, trg_tok) if len(s.split(' ')) + len(t.split(' ')) < cutoff]
    src_tok_clean = [s for (s, _t) in src_trg_clean]
    trg_tok_clean = [t for (_s, t) in src_trg_clean]

    return src_tok_clean, trg_tok_clean
    
def main():
    """ main function """
    # read argument - file with data
    parser = argparse.ArgumentParser(description='Splits a parallel corpus into train, test and dev sets.')
    parser.add_argument('-s', '--source', required=True, help='The source-language file.')
    parser.add_argument('-t', '--target', required=True, help='The target-language file.')
    parser.add_argument('-l', '--src-language', required=False, help='The source language.', default='en')
    parser.add_argument('-k', '--trg-language', required=False, help='The target language.', default='nl')
    parser.add_argument('-c', '--cutoff', required=False, help='Cleaning cutoff.', default='160')
    parser.add_argument('-z', '--size', required=False, help='The size for the test and dev sets. The train set is all that remains.', default='1000')

    args = parser.parse_args()
    
    # 1. Read and split the files:
    logging.info("Spliting ...")
    src, trg = split_ttd(args.source, args.target, int(args.size))
    logging.info("done.")
    
    # 2. Tokenize the splits:
    logging.info("Tokenizing ...")
    src_tok = tokenize(src, args.src_language)
    trg_tok = tokenize(trg, args.trg_language)
    logging.info("done.")
    
    # 3. Clean the training corpus:
    logging.info("Cleaning ...")
    src_tok['train'], trg_tok['train'], clean(src_tok['train'], trg_tok['train'], int(args.cutoff))
    logging.info("done.")
    
    # 4. now we are ok to save the data into train, test and dev files
    for split in ['train', 'test', 'dev']:
        src_out_filename = '.'.join([args.source, split, 'tok-clean', 'src']) 
        trg_out_filename = '.'.join([args.target, split, 'tok-clean', 'trg'])
        with codecs.open(src_out_filename, 'w', 'utf8') as srcOutFile, codecs.open(trg_out_filename, 'w', 'utf8') as trgOutFile:
            srcOutFile.write('\n'.join(src[split]) + '\n')
            trgOutFile.write('\n'.join(trg[split]) + '\n')
    logging.info("All done.")
# That should be it.    
    
if __name__ == "__main__":
    main()
