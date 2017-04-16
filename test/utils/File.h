#ifndef __MIRAI_FILE_H__
#define __MIRAI_FILE_H__

#include <cstdint>
#include <fstream>
#include <string>

inline uint64_t GetFileSize(const std::string &file_path)
{
    std::ifstream file(file_path, std::ios::binary | std::ios::ate);

    return file.tellg();
}

inline uint64_t GetFileSize(const std::wstring &file_path)
{
    std::ifstream file(file_path, std::ios::binary | std::ios::ate);

    return file.tellg();
}

#endif