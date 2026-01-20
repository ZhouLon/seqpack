#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <vector>

struct FastaStats {
    int sequenceCount;
    long long totalLength;
    double processingTimeMs;
};

FastaStats analyzeFasta(const std::string& filepath, bool verbose = false) {
    auto start = std::chrono::high_resolution_clock::now();
    
    FastaStats stats = {0, 0, 0.0};
    std::ifstream file(filepath);
    
    if (!file.is_open()) {
        throw std::runtime_error("无法打开文件: " + filepath);
    }
    
    std::string line;
    int currentSeqLength = 0;
    
    while (std::getline(file, line)) {
        if (line.empty()) continue;
        
        if (line[0] == '>') {
            stats.sequenceCount++;
            if (verbose && currentSeqLength > 0) {
                std::cout << "序列长度: " << currentSeqLength << std::endl;
            }
            currentSeqLength = 0;
        } else {
            currentSeqLength += line.length();
            stats.totalLength += line.length();
        }
    }
    
    file.close();
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    stats.processingTimeMs = duration.count();
    
    return stats;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "使用方法: " << argv[0] << " <fasta文件路径> [--verbose]" << std::endl;
        return 1;
    }
    
    bool verbose = false;
    if (argc > 2 && std::string(argv[2]) == "--verbose") {
        verbose = true;
    }
    

        FastaStats stats = analyzeFasta(argv[1], verbose);
        
        std::cout << "\n========== FASTA 分析结果 ==========" << std::endl;
        std::cout << "文件: " << argv[1] << std::endl;
        std::cout << "序列数量: " << stats.sequenceCount << std::endl;
        std::cout << "总碱基数: " << stats.totalLength << std::endl;
        std::cout << "处理时间: " << stats.processingTimeMs << " 毫秒" << std::endl;
        
        if (stats.sequenceCount > 0) {
            std::cout << "平均序列长度: " << static_cast<double>(stats.totalLength) / stats.sequenceCount << std::endl;
            std::cout << "处理速度: " << stats.totalLength / stats.processingTimeMs << " 碱基/毫秒" << std::endl;
        }
    
    return 0;
}