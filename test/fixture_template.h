#ifndef __FIXTURE_TEMPLATE_H__
#define __FIXTURE_TEMPLATE_H__

#include "gtest/gtest.h"

class TestTemplate : public ::testing::Test
{
public:
  static void SetUpTestCase();
  static void TearDownTestCase();

protected:
  virtual void SetUp();
  virtual void TearDown();
};

// Replace a parameter type to that you want to test
class ParameterizedTestTemplate : public ::testing::TestWithParam<int>
{
public:
  static void SetUpTestCase();
  static void TearDownTestCase();

protected:
  virtual void SetUp();
  virtual void TearDown();
};

// Replace parameters type to that you want to test
class CombineParameterizedTestTemplate
    : public ::testing::TestWithParam<std::tuple<int, int>>
{
public:
  static void SetUpTestCase();
  static void TearDownTestCase();

protected:
  virtual void SetUp();
  virtual void TearDown();
};

#endif
