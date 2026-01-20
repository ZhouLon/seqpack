import ctypes
import os
import sys
from pathlib import Path
import argparse

class FastaReader:
    def __init__(self, lib_path=None):
        """
        初始化FASTA读取器
        
        参数:
            lib_path: C库的路径，如果为None则尝试自动查找
        """
        if lib_path is None:
            # 尝试在常见位置查找库
            possible_paths = [
                './libfastaparser.so',
                './fastaparser.so',
                './libfastaparser.dylib',
                './fastaparser.dylib',
                './fastaparser.dll',
                './build/lib.*/fastaparser.*'
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    lib_path = path
                    break
        
        if lib_path is None or not os.path.exists(lib_path):
            raise FileNotFoundError(f"C库未找到: {lib_path}")
        
        # 加载C库
        self.lib = ctypes.CDLL(lib_path)
        
        # 设置函数参数和返回类型
        self.lib.read_fasta_file.argtypes = [ctypes.c_char_p]
        self.lib.read_fasta_file.restype = ctypes.c_char_p
        
        self.lib.free_string.argtypes = [ctypes.c_char_p]
        self.lib.free_string.restype = None
    
    def read_fasta(self, filepath):
        """
        读取FASTA文件
        
        参数:
            filepath: FASTA文件路径
            
        返回:
            字符串形式的序列信息
        """
        # 检查文件是否存在
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        # 调用C函数
        filepath_bytes = filepath.encode('utf-8')
        result_ptr = self.lib.read_fasta_file(filepath_bytes)
        
        if result_ptr is None:
            raise RuntimeError("无法读取FASTA文件")
        
        # 将C字符串转换为Python字符串
        result = ctypes.string_at(result_ptr).decode('utf-8')
        
        # 释放C分配的内存
        self.lib.free_string(result_ptr)
        
        return result
    
    def read_fasta_as_dict(self, filepath):
        """
        读取FASTA文件并返回字典（序列ID -> 序列）
        
        参数:
            filepath: FASTA文件路径
            
        返回:
            字典，键为序列ID，值为序列字符串
        """
        raw_result = self.read_fasta(filepath)
        
        # 解析原始结果（这里可以根据需要修改解析逻辑）
        # 这是一个简单的示例实现
        sequences = {}
        current_id = None
        current_seq = []
        
        lines = raw_result.split('\n')
        for line in lines:
            if line.startswith('Sequence: '):
                # 保存前一个序列
                if current_id is not None and current_seq:
                    sequences[current_id] = ''.join(current_seq)
                
                # 开始新序列
                current_id = line[10:].strip()  # 去掉"Sequence: "
                current_seq = []
            elif line.startswith('Data: '):
                current_seq.append(line[6:])  # 去掉"Data: "
        
        # 保存最后一个序列
        if current_id is not None and current_seq:
            sequences[current_id] = ''.join(current_seq)
        
        return sequences

# 命令行接口
def main():
    
    
    parser = argparse.ArgumentParser(description='读取FASTA文件')
    parser.add_argument('filepath', help='FASTA文件路径')
    parser.add_argument('--library', '-l', help='C库路径', default=None)
    
    args = parser.parse_args()
    
    try:
        reader = FastaReader(args.library)
        result = reader.read_fasta(args.filepath)
        print(result)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()