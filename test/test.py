import sys
import time
from pathlib import Path


#从src加载包
from seqpack.read_file import ReadMethod as rm



def main():
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("使用方法: python fasta_reader.py <fasta文件路径>")
        print("示例: python fasta_reader.py sequences.fasta")
        sys.exit(1)
    filepath = sys.argv[1]
    print(f"正在读取FASTA文件: {filepath}")
    # 读取并显示FASTA文件
    sequences = rm.read_from_biopython(filepath)
    
    print(f"总序列数: {len(sequences)}")


if __name__ == "__main__":
    time0=time.time()
    main()
    print("总用时: %.2f 秒"%(time.time()-time0))

