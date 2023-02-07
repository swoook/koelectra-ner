class Example:
    def __init__(self):
        self._word_sequence = list()
        self._label_sequence = list()
        self._negative = '-'
        self._begin = '_B'
        self._consecutive = '_I'
        self.seq_len_threshold = 4
        self._marks = ['.', '!', '?']
        
    def _create_positive_subsequence(self, substring, label):
        words = substring.split()
        labels = [''.join([label, self._begin])]
        for _ in range(len(words) - 1): labels.append(''.join([label, self._consecutive]))
        return words, labels

    def _create_negative_subsequence(self, substring):
        words = substring.split()
        labels = [self._negative for _ in range(len(words))]
        return words, labels
    
    def _extend_subsequence(self, subsequence):
        self._word_sequence.extend(subsequence[0])
        self._label_sequence.extend(subsequence[1])
    
    def _create_subsequence(self, substring, label):
        subsequence = self._create_negative_subsequence(substring) if label == self._negative else self._create_positive_subsequence(substring, label)
        self._extend_subsequence(subsequence)
        
    def _separate_end_mark(self):
        word = self._word_sequence.pop()
        self._word_sequence.append(word[:-1])
        self._word_sequence.append(word[-1])
        self._label_sequence.append(self._negative)
    
    def _initialize(self):
        self._word_sequence = list()
        self._label_sequence = list()

    def convert(self, example):
        self._initialize()
        
        if not example['NE']:
            self._create_subsequence(example['text'], '-')
        
        else:
            entities_sorted = sorted(example['NE'], key=lambda item: item['begin'])

            if entities_sorted[0]['begin'] > 0:
                tail_idx = entities_sorted[0]['begin']
                substring = example['text'][:tail_idx]
                self._create_subsequence(substring, '-')

            for idx, entity in enumerate(entities_sorted[:-1]):
                head_idx = entity['begin']
                tail_idx = entity['end']
                substring = example['text'][head_idx:tail_idx]
                self._create_subsequence(substring, entity['type'])

                head_idx = entities_sorted[idx]['end']
                tail_idx = entities_sorted[idx+1]['begin']
                substring = example['text'][head_idx:tail_idx]
                self._create_subsequence(substring, '-')

            head_idx = entities_sorted[-1]['begin']
            tail_idx = entities_sorted[-1]['end']
            substring = example['text'][head_idx:tail_idx]
            self._create_subsequence(substring, entities_sorted[-1]['type'])

            if entities_sorted[-1]['end'] < len(example['text']):
                head_idx = entities_sorted[-1]['end']
                tail_idx = len(example['text'])
                substring = example['text'][head_idx:tail_idx]
                self._create_subsequence(substring, '-')
        
        if not len(self._label_sequence) >= self.seq_len_threshold:
            return None
        
        if (self._label_sequence[-1] == self._negative) and (self._word_sequence[-1][-1] in self._marks): 
            self._separate_end_mark()
        
        return ' '.join(self._word_sequence), ' '.join(self._label_sequence)