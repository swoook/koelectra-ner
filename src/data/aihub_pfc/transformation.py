from copy import deepcopy


def create_label_sequence(example):
    result = list()
    
    entities_sorted = sorted(example['NE'], key=lambda item: item['begin'])
    
    if entities_sorted[0]['begin'] > 0:
        tail_idx = entities_sorted[0]['begin']
        labels.append(
            {
                'id': None, 
                'entity': example['text'][:tail_idx], 
                'type': 'O', 
                'begin': 0, 
                'end': tail_idx,
            }
        )
        
    for idx, entity in enumerate(entities_sorted[:-1]):
        labels.append(deepcopy(entity))
        head_idx = entities_sorted[idx]['end']
        tail_idx = entities_sorted[idx+1]['begin']
        labels.append(
            {
                'id': None, 
                'entity': example['text'][head_idx:tail_idx], 
                'type': 'O', 
                'begin': head_idx, 
                'end': tail_idx,
            }
        )
        
    labels.append(deepcopy(entities_sorted[-1]))
    if entities_sorted[-1]['end'] < len(example['text']):
        head_idx = entities_sorted[-1]['end']
        tail_idx = len(example['text'])
        labels.append(
            {
                'id': None, 
                'entity': example['text'][head_idx:tail_idx], 
                'type': 'O', 
                'begin': head_idx, 
                'end': tail_idx,
            }
        )
    
    return result