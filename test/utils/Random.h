#ifndef __MIRAI_RANDOM_H__
#define __MIRAI_RANDOM_H__

#include <random>
#include <string>

template <typename T>
class RandomNumberGenerator
{
  public:
    RandomNumberGenerator(T min, T max, unsigned int seed = 0)
        : mt_(seed), dist_(min, max) {}

    virtual ~RandomNumberGenerator() = default;

    T GetRandomValue()
    {
        return dist_(mt_);
    }

  private:
    std::mt19937 mt_;
    std::uniform_int_distribution<T> dist_;
};

template <typename T, typename C>
class RandomStringGenerator
{
  public:
    RandomStringGenerator(unsigned int seed = 0)
        : mt_(seed), dist_ascii_char_(33, 126) {}

    virtual ~RandomStringGenerator() = default;

    C GetRandomChar()
    {
        return dist_ascii_char_(mt_);
    }

    T GetRandomString(unsigned int length)
    {
        T random_str;

        random_str.reserve(length);
        for (unsigned int i = 0; i < length; i++)
        {
            random_str += GetRandomChar();
        }

        return random_str;
    }

  private:
    std::mt19937 mt_;
    std::uniform_int_distribution<> dist_ascii_char_;
};

using RandomStdStringGenerator = RandomStringGenerator<std::string, char>;

#endif