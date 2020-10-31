from onmt.translate.translator import build_translator
from argparse import Namespace

path = 'model\\model_step_50000.pt'

opt = Namespace(alpha=0.0, batch_type='sents', beam_size=5, beta=-0.0, block_ngram_repeat=0, coverage_penalty='none',
                data_type='text', dump_beam='', fp32=False, gpu=-1, ignore_when_blocking=[], length_penalty='none',
                max_length=100, max_sent_length=None, min_length=0, models=[path],
                n_best=1, output='model\\output.txt', phrase_table='', random_sampling_temp=1.0, random_sampling_topk=1,
                ratio=-0.0, replace_unk=False, report_align=False, report_time=False, seed=829,
                stepwise_penalty=False, tgt=None, verbose=False, tgt_prefix=None)
translator_object = build_translator(opt, report_score=True)


#
# translator.translate(['Whether you are a junior, senior, project manager, or a top-level manager with 20 years of experience, software project time estimation never becomes easy. No one no matter how experienced or genius they are can claim to know for sure the exact time a software project would take.This problem is especially prevalent in software engineering, but other engineering disciplines are also known to suffer from the same downfall. So while this article focuses on software engineering, it also applies to other disciplines, to an extent.'], batch_size=1)

from threading import Lock

output_file_lock = Lock()

def translate(text: str):
    output_file_lock.acquire()
    translator_object.translate([text], batch_size=1)
    return get_output()





def get_output():
    '''Get the output from the output.txt threat save'''

    try:
        with open('model/output.txt', 'r+') as output:
            text = output.read()
    finally:
        output_file_lock.release()
    return text
