import sys
import time
from Bio import SeqIO

def read_fasta(filepath):
    """读取FASTA文件并返回内容"""
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
    
def read_fasta_bio(filepath):
    fasta_sequences = SeqIO.parse(filepath, "fasta")
    sequences = []
    for seq_record in fasta_sequences:
        name, sequence = seq_record.id, str(seq_record.seq)
        sequences.append(sequence)
    return sequences

def main():
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("使用方法: python fasta_reader.py <fasta文件路径>")
        print("示例: python fasta_reader.py sequences.fasta")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    print(f"正在读取FASTA文件: {filepath}")
    
    # 读取并显示FASTA文件
    sequences = read_fasta(filepath)
    
    print(f"总序列数: {len(sequences)}")


if __name__ == "__main__":
    time0=time.time()
    main()
    print("总用时: %.2f 秒"%(time.time()-time0))