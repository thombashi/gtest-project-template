#include "path.h"
#include <stdio.h>

std::string GetTempPath()
{
    char temp_name_buf[L_tmpnam_s];
    errno_t err;

    err = tmpnam_s(temp_name_buf, L_tmpnam_s);
    if (err)
    {
        printf("Error occurred creating unique filename.\n");
    }

    return std::string(temp_name_buf);
}
