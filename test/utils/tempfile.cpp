#include "tempfile.h"

#include "path.h"
#include <fstream>
#include <stdio.h>

TempFile::TempFile() : temp_file_path_(GetTempPath())
{
    std::ofstream ofs(temp_file_path_, std::ios::out);
}

TempFile::~TempFile()
{
    remove(temp_file_path_.c_str());
}

std::unique_ptr<TempFile> TempFileFactory::CreateTempFileWithData(size_t file_size)
{
    auto tempfile = std::unique_ptr<TempFile>(
        new TempFileWithData(file_size, random_str_generator_));

    return tempfile;
}