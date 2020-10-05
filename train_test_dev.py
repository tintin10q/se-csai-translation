import os
import codecs

print(os.getcwd())
print('start')
with codecs.open(os.path.join('raw data', 'europarl-v7.nl-en.en'), 'r', 'utf8') as srcFile, codecs.open(os.path.join('raw data', 'europarl-v7.nl-en.nl'), 'r', 'utf8') as trgFile:
    src1m = srcFile.readlines()
    trg1m = trgFile.readlines()
print('Got here 1')
src = {}
trg = {}

from sklearn.model_selection import train_test_split
src['train'], src['test'], trg['train'], trg['test'] = train_test_split(src1m, trg1m, shuffle=True, test_size=2000, random_state=42)
src['dev'], src['test'], trg['dev'], trg['test'] = train_test_split(src['test'], trg['test'], shuffle=True, test_size=1000, random_state=42)
print('got here 2')

from sacremoses import MosesTokenizer
mt_src, mt_trg =  MosesTokenizer(lang='en'), MosesTokenizer(lang='nl')
print('got here 3 this will take long')

counter = 0
print("src len is", len(src))
for split in src:
    counter += 1
    print(counter)
    src[split] = [mt_src.tokenize(sent.rstrip(), return_str=True, escape=False) for sent in src[split]]
    trg[split] = [mt_trg.tokenize(sent.rstrip(), return_str=True, escape=False) for sent in trg[split]]
print('got here 4')

# now let's clean the training data
src_trg_clean = [(s, t) for s, t in zip(src['train'], trg['train']) if len(s.split(' ')) + len(t.split(' ')) < 160]
src['train'] = [s for (s, _t) in src_trg_clean]
trg['train'] = [t for (_s, t) in src_trg_clean]
print('got here 5')

# now we are ok to save the data into a train, test and dev files
for split in src:
    with codecs.open(os.path.join('EN-NL', 'data', split + '.src'), 'w', 'utf8') as srcOutFile, codecs.open(os.path.join('EN-NL', 'data', split + '.trg'), 'w', 'utf8') as trgOutFile:
        srcOutFile.write('\n'.join(src[split]) + '\n')
        trgOutFile.write('\n'.join(trg[split]) + '\n')
print('got here 7 all done')

# That should be it.
