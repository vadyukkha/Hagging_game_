Есть ограниченное количество предметов на игровом поле: одна шапка (Hat), две книги (Books), 3 мяча (Balls) и есть два игрока (A и B), для которых ценность каждого предмета своя и которые хотят поделить эти предметы между собой с получением максимальной выгод, сумма предметов у каждого игрока равна 10. Например у игрока может быть 1 шапка по 5, 2 книги по 1 и 3 шара по 1, всего получается 1*5+2*1+3*1. Игрок не знает стоимостей предметов у противника. Один может предлагать обмен второму, а второй первому. Такие обмены предлагаются поочередно, всего может быть 5 предложений обмена. Нужно написать программу, а точнее специализированную функцию на языке программирования С++. Нужно написать стратегию, которая сможет договариваться об обмене наилучшим образом с получением максимальной выгоды с другой стратегией. 

Написать функцию:
```
#ifdef _WIN32 
#define EXPORT __declspec(dllexport) 
#else 
#define EXPORT __attribute__((visibility("default"))) 
#endif 

extern "C" EXPORT int decide(int turn, int cost_hat, int cost_book, int cost_ball, int count_hat, int count_book, int count_ball)
```

Где turn - номер шага от 0 до 5,
hatCost, bookCost, ballCost - стоимости предметов игрока, то есть мои предметы,
hatCount, bookCount, ballCount - количество предметов, которые отдает противник.

Эта функция должна вернуть 200, если такой обмен удовлетворяет стратегии, иначе нужно отправить число hbb, которое означает то количество, которое мы хотим предложить противнику. Например число 12 означает, что я хочу отдать противнику 0 шапок, 1 книгу и 2 мяча. Соответственно я хочу забрать 1 шапку и 1 книгу и 1 мяч. Если функция противника посчитает такой обмен выгодным, то она вернет 200 и обмен закончится. Главная задача - совершить обмен, распределение предметов за 5 шагов turn. Программа должна анализировать предложения об обмене и прогнозировать стоимость предметов противника. Стратегия считается успешной, если обмен состоится, желательно с максимально возможной выгодной. В рамках этого проекта, вы можете играть только с ботами.