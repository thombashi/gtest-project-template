#ifndef __MIRAI_TEMPFILE_H__
#define __MIRAI_TEMPFILE_H__

#include "Random.h"
#include <memory>
#include <string>

class TempFile
{
public:
  TempFile();

  virtual ~TempFile();

  std::string GetFileName() const { return temp_file_path_; }

protected:
  std::string temp_file_path_;

private:
  TempFile(const TempFile &) = delete;
  TempFile(TempFile &&) = delete;
  TempFile &operator=(const TempFile &) = delete;
  TempFile &operator=(TempFile &&) = delete;
};

class TempFileWithData : public TempFile
{
public:
  template <typename T, typename C>
  TempFileWithData(
      size_t file_size,
      RandomStringGenerator<T, C> &random_str_generator = RandomStdStringGenerator()) : TempFile()
  {
    std::ofstream ofs(temp_file_path_, std::ios::out);
    ofs << random_str_generator.GetRandomString(file_size);
  }

  virtual ~TempFileWithData() = default;

private:
  TempFileWithData() = delete;
  TempFileWithData(const TempFileWithData &) = delete;
  TempFileWithData(TempFileWithData &&) = delete;
  TempFileWithData &operator=(const TempFileWithData &) = delete;
  TempFileWithData &operator=(TempFileWithData &&) = delete;
};

class TempFileFactory
{
public:
  TempFileFactory() = default;

  virtual ~TempFileFactory() = default;

  std::unique_ptr<TempFile> CreateTempFileWithData(size_t file_size);

private:
private:
  TempFileFactory(const TempFileFactory &) = delete;
  TempFileFactory(TempFileFactory &&) = delete;
  TempFileFactory &operator=(const TempFileFactory &) = delete;
  TempFileFactory &operator=(TempFileFactory &&) = delete;

  RandomStdStringGenerator random_str_generator_;
};

#endif
