#include "fixture_template.h"
#include "utils/gtestio.h"
#include "gtest/gtest.h"

using ::testing::Values;
using ::testing::ValuesIn;

TEST_P(ParameterizedFixtureTemplate, OneParamTemplate)
{
    const auto param0 = GetParam();

    EXPECT_TRUE(false) << "replace this arbitrary test content";
}

INSTANTIATE_TEST_CASE_P(
    OneParamInstantiate,
    ParameterizedFixtureTemplate,
    Values(1, 2, 3));
