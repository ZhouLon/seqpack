#ifndef FASTA_PARSER_H
#define FASTA_PARSER_H

#define MAX_LINE_LENGTH 1024

#ifdef __cplusplus
extern "C" {
#endif

// 读取FASTA文件的函数声明
char* read_fasta_file(const char* filepath);
void free_string(char* str);

#ifdef __cplusplus
}
#endif

#endif // FASTA_PARSER_H