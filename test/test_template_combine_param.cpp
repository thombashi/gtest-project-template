#include "fixture_template.h"
#include "utils/gtestio.h"
#include "gtest/gtest.h"

using ::testing::Values;
using ::testing::ValuesIn;
using ::testing::Combine;

TEST_P(CombineParameterizedTestTemplate, TwoParamTemplate)
{
    const auto param0 = std::get<0>(GetParam());
    const auto param1 = std::get<1>(GetParam());

    EXPECT_TRUE(false) << "replace this arbitrary test content";
}

INSTANTIATE_TEST_CASE_P(
    TwoParamInstantiate,
    CombineParameterizedTestTemplate,
    Combine(
        Values(1, 2, 3),
        Values(11, 12, 13)));
