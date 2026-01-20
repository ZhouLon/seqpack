import random
import gzip

def generate_huge_fasta(filename, total_size_gb=1):
    """生成GB级别的大型FASTA文件"""
    bases = ['A', 'T', 'C', 'G']
    seq_num = 1
    target_bytes = total_size_gb * 1024 * 1024 * 1024
    
    with open(filename, 'w') as f:
        current_size = 0
        
        while current_size < target_bytes:
            # 生成序列（长度500-5000）
            seq_length = random.randint(500, 5000)
            sequence = ''.join(random.choice(bases) for _ in range(seq_length))
            
            # 写入记录
            header = f">sequence_{seq_num}_length={seq_length}\n"
            f.write(header)
            current_size += len(header.encode())
            
            # 分多行写入序列
            for i in range(0, len(sequence), 80):
                line = sequence[i:i+80] + "\n"
                f.write(line)
                current_size += len(line.encode())
            
            seq_num += 1
            
            # 进度显示
            if seq_num % 1000 == 0:
                print(f"已生成 {seq_num} 条序列，文件大小: {current_size/1024/1024:.2f} MB")

# 生成1GB的FASTA文件（警告：可能需要一些时间）
generate_huge_fasta("huge_sequences.fasta", total_size_gb=0.1)  