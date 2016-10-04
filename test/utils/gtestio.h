#ifndef __GTESTIO_H__
#define __GTESTIO_H__

#include "gtest/gtest.h"

namespace testing
{
namespace internal
{
enum GTestColor
{
    COLOR_DEFAULT,
    COLOR_RED,
    COLOR_GREEN,
    COLOR_YELLOW
};

extern void ColoredPrintf(GTestColor color, const char *fmt, ...);
}
}

template <typename... Args>
static void gtestprintf(const std::string &format, Args const &... args)
{
    testing::internal::ColoredPrintf(
        testing::internal::COLOR_GREEN, "[          ] ");
    testing::internal::ColoredPrintf(
        testing::internal::COLOR_YELLOW, format.c_str(), args...);
}

class GTestCout : public std::stringstream
{
  public:
    ~GTestCout()
    {
        gtestprintf("%s", str().c_str());
    }
};

class GTestCerr : public std::stringstream
{
  public:
    ~GTestCerr()
    {
        testing::internal::ColoredPrintf(
            testing::internal::COLOR_RED, "[          ] ");
        testing::internal::ColoredPrintf(
            testing::internal::COLOR_RED, str().c_str());
    }
};

#define gtestcout GTestCout()
#define gtestcerr GTestCerr()

#endif
