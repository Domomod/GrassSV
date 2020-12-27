class FastqInstance:
    def __init__(self, seq_id, raw_seq, quality, number):
        self.seq_id = seq_id
        self.raw_seq = raw_seq
        self.quality = quality
        self.number = number  # 1 or 2

    def __str__(self):
        return '@{}/{}\n{}\n+\n{}\n'.format(self.seq_id, self.number, self.raw_seq, self.quality)

    def __repr__(self):
        return str(self)
