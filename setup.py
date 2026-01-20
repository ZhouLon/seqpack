from setuptools import setup, find_packages

setup(
    name="seqpack",
    version="0.0.1",
    author="ZhouLong",
    description="一个快速存储加载FASTA文件的工具包",
    
    # 关键：指定包在 src 目录下
    package_dir={"": "src"},  
    packages=find_packages(where="src"),
    
    install_requires=[
        "biopython",
    ],
)