import sys
import time
from Bio import SeqIO

class ReadMethod:

    def read_from_python(filepath):
        """用python基础代码读取FASTA文件并返回内容"""
        sequences = []
        current_header = None
        current_sequence = []
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:  # 跳过空行
                    continue
                if line.startswith('>'):  # 序列头部
                    if current_header:  # 保存之前的序列
                        sequences.append((current_header, ''.join(current_sequence)))
                        current_sequence = []
                    
                    current_header = line  # 保存新头部
                else:
                    current_sequence.append(line)
            
            # 添加最后一个序列
            if current_header:
                sequences.append((current_header, ''.join(current_sequence)))
        return sequences

    def read_from_biopython(filepath):
        """用biopython的api读取FASTA文件并返回内容"""
        fasta_sequences = SeqIO.parse(filepath, "fasta")
        sequences = []
        for seq_record in fasta_sequences:
            name, sequence = seq_record.id, str(seq_record.seq)
            sequences.append(sequence)
        return sequences