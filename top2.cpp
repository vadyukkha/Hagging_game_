#include <iostream>

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT __attribute__((visibility("default")))
#endif

extern "C" EXPORT int decide(int turn, int hat_cost, int book_cost, int ball_cost, int hat_count, int book_count, int ball_count)
{
    switch (turn)
    {
    case 0:
        return 120;
        break;
    case 1:
        return 120;
        break;
    case 2:
        if (ball_count == 3) return 200;
        return 121;
        break;
    case 3:
        if (ball_count == 3) return 200;
        return 121; 
        break;
    case 4:
        if (ball_count == 3) return 200;
        return 122;
        break;
    case 5:
        if (ball_count == 3) return 200;
        return 122;
        break;
    return 200;
    }
}