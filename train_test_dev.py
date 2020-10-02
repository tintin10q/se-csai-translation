import os
import codecs
with codecs.open(os.path.join('raw_data', 'Europarl.en-nl.en'), 'r', 'utf8') as srcFile, codecs.open(os.path.join('raw_data', 'Europarl.en-nl.nl'), 'r', 'utf8') as trgFile:
    src1m = srcFile.readlines()[:1002000]
    trg1m = trgFile.readlines()[:1002000]

src = {}
trg = {}

from sklearn.model_selection import train_test_split
src['train'], src['test'], trg['train'], trg['test'] = train_test_split(src1m, trg1m, shuffle=True, test_size=2000, random_state=42)
src['dev'], src['test'], trg['dev'], trg['test'] = train_test_split(src['test'], trg['test'], shuffle=True, test_size=1000, random_state=42)

from sacremoses import MosesTokenizer
mt_src, mt_trg =  MosesTokenizer(lang='en'), MosesTokenizer(lang='nl')

for split in src:
    src[split] = [mt_src.tokenize(sent.rstrip(), return_str=True, escape=False) for sent in src[split]]
    trg[split] = [mt_trg.tokenize(sent.rstrip(), return_str=True, escape=False) for sent in trg[split]]

# now let's clean the training data
src_trg_clean = [(s, t) for s, t in zip(src['train'], trg['train']) if len(s.split(' ')) + len(t.split(' ')) < 160]
src['train'] = [s for (s, _t) in src_trg_clean]
trg['train'] = [t for (_s, t) in src_trg_clean]

# now we are ok to save the data into a train, test and dev files
for split in src:
    with codecs.open(os.path.join('EN-NL', 'data', split + '.src'), 'w', 'utf8') as srcOutFile, codecs.open(os.path.join('EN-NL', 'data', split + '.trg'), 'w', 'utf8') as trgOutFile:
        srcOutFile.write('\n'.join(src[split]) + '\n')
        trgOutFile.write('\n'.join(trg[split]) + '\n')

# That should be it.
