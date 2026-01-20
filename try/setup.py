from distutils.core import setup, Extension
import sys

# 定义C扩展模块
fasta_module = Extension(
    'fastaparser',
    sources=['fasta_parser.c'],
    include_dirs=['.'],
    depends=['fasta_parser.h'],
    extra_compile_args=['-O2', '-Wall'] if sys.platform != 'win32' else [],
)

setup(
    name='fasta_reader',
    version='1.0',
    description='Python调用C读取FASTA文件',
    ext_modules=[fasta_module],
    py_modules=['fasta_reader'],
)