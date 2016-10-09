#ifndef __MIRAI_FILE_H__
#define __MIRAI_FILE_H__

#include <fstream>

inline long long GetFileSize(const std::string &file_path)
{
    std::ifstream file(file_path, std::ios::binary | std::ios::ate);

    return file.tellg();
}

#endif