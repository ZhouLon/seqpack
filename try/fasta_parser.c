#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "fasta_parser.h"

// 读取FASTA文件并返回序列字符串
char* read_fasta_file(const char* filepath) {
    FILE* file = fopen(filepath, "r");
    if (file == NULL) {
        return NULL;
    }
    
    // 第一次遍历，获取所需内存大小
    char line[MAX_LINE_LENGTH];
    long total_length = 0;
    int in_sequence = 0;
    
    while (fgets(line, sizeof(line), file) != NULL) {
        // 去除换行符
        line[strcspn(line, "\n")] = '\0';
        line[strcspn(line, "\r")] = '\0';
        
        if (line[0] == '>') {
            // 这是序列头，跳过
            in_sequence = 0;
        } else if (strlen(line) > 0) {
            // 这是序列行
            total_length += strlen(line);
            in_sequence = 1;
        }
    }
    
    // 重新读取文件以提取序列
    rewind(file);
    
    // 分配内存（+1 用于 null 终止符）
    char* result = (char*)malloc(total_length + 1);
    if (result == NULL) {
        fclose(file);
        return NULL;
    }
    result[0] = '\0';
    
    in_sequence = 0;
    while (fgets(line, sizeof(line), file) != NULL) {
        line[strcspn(line, "\n")] = '\0';
        line[strcspn(line, "\r")] = '\0';
        
        if (line[0] == '>') {
            in_sequence = 0;
            // 如果是第一个序列，可以添加标题信息
            if (strlen(result) == 0) {
                strcat(result, "Sequence: ");
                strcat(result, line + 1);  // 跳过 '>'
                strcat(result, "\n");
            }
        } else if (strlen(line) > 0) {
            if (in_sequence) {
                strcat(result, line);
            } else {
                strcat(result, "Data: ");
                strcat(result, line);
                in_sequence = 1;
            }
        }
    }
    
    fclose(file);
    return result;
}

// 释放内存函数
void free_string(char* str) {
    if (str != NULL) {
        free(str);
    }
}