from copy import deepcopy


def create_positive_subsequence(substring, label):
    words = substring.split()
    labels = [''.join([label, '_B'])]
    for idx in range(len(words) - 1): labels.append(''.join([label, '_I']))
    return words, labels

def create_negative_subsequence(substring, label):
    words = substring.split()
    labels = ['-' for _ in range(len(words))]
    return words, labels

def create_subsequence(substring, label):
    if label == '-': return create_negative_subsequence(substring, label)
    else: return create_positive_subsequence(substring, label)

def create_word_label_sequence(example):
    words = list()
    labels = list()
    
    entities_sorted = sorted(example['NE'], key=lambda item: item['begin'])
    
    if entities_sorted[0]['begin'] > 0:
        tail_idx = entities_sorted[0]['begin']
        substring = example['text'][:tail_idx]
        subsequence = create_subsequence(substring, '-')
        words.extend(subsequence[0])
        labels.extend(subsequence[1])
        
    for idx, entity in enumerate(entities_sorted[:-1]):
        head_idx = entity['begin']
        tail_idx = entity['end']
        substring = example['text'][head_idx:tail_idx]
        subsequence = create_subsequence(substring, entity['type'])
        words.extend(subsequence[0])
        labels.extend(subsequence[1])
        
        head_idx = entities_sorted[idx]['end']
        tail_idx = entities_sorted[idx+1]['begin']
        substring = example['text'][head_idx:tail_idx]
        subsequence = create_subsequence(substring, '-')
        words.extend(subsequence[0])
        labels.extend(subsequence[1])
    
    head_idx = entities_sorted[-1]['begin']
    tail_idx = entities_sorted[-1]['end']
    substring = example['text'][head_idx:tail_idx]
    subsequence = create_subsequence(substring, entities_sorted[-1]['type'])
    words.extend(subsequence[0])
    labels.extend(subsequence[1])
    
    if entities_sorted[-1]['end'] < len(example['text']):
        head_idx = entities_sorted[-1]['end']
        tail_idx = len(example['text'])
        substring = example['text'][head_idx:tail_idx]
        subsequence = create_subsequence(substring, '-')
        words.extend(subsequence[0])
        labels.extend(subsequence[1])
    
    return words, labels