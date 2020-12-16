#!/usr/bin/env python3

# --- Day 6: Custom Customs ---
# As your flight approaches the regional airport where you'll switch to a much larger plane, customs declaration forms are distributed to the passengers.
# The form asks a series of 26 yes-or-no questions marked a through z. All you need to do is identify the questions for which anyone in your group answers "yes". Since your group is just you, this doesn't take very long.
# However, the person sitting next to you seems to be experiencing a language barrier and asks if you can help. For each of the people in their group, you write down the questions for which they answer "yes", one per line. For example:
# abcx
# abcy
# abcz
# In this group, there are 6 questions to which anyone answered "yes": a, b, c, x, y, and z. (Duplicate answers to the same question don't count extra; each question counts at most once.)
# Another group asks for your help, then another, and eventually you've collected answers from every group on the plane (your puzzle input). Each group's answers are separated by a blank line, and within each group, each person's answers are on a single line. For example:
# check day_6_answers_example.txt
# This list represents answers from five groups:
# The first group contains one person who answered "yes" to 3 questions: a, b, and c.
# The second group contains three people; combined, they answered "yes" to 3 questions: a, b, and c.
# The third group contains two people; combined, they answered "yes" to 3 questions: a, b, and c.
# The fourth group contains four people; combined, they answered "yes" to only 1 question, a.
# The last group contains one person who answered "yes" to only 1 question, b.
# In this example, the sum of these counts is 3 + 3 + 3 + 1 + 1 = 11.
# For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?

# Your puzzle answer was 6782.

# --- Part Two ---
# As you finish the last group's customs declaration, you notice that you misread one word in the instructions:
# You don't need to identify the questions to which anyone answered "yes"; you need to identify the questions to which everyone answered "yes"!
# Using the same example as above:
# This list represents answers from five groups:
# In the first group, everyone (all 1 person) answered "yes" to 3 questions: a, b, and c.
# In the second group, there is no question to which everyone answered "yes".
# In the third group, everyone answered yes to only 1 question, a. Since some people did not answer "yes" to b or c, they don't count.
# In the fourth group, everyone answered yes to only 1 question, a.
# In the fifth group, everyone (all 1 person) answered "yes" to 1 question, b.
# In this example, the sum of these counts is 3 + 0 + 1 + 1 + 1 = 6.
# For each group, count the number of questions to which everyone answered "yes". What is the sum of those counts?
# Your puzzle answer was 3596.

from functools import reduce


def sum_count_of_yes(answers_str):
    """
    Sum of the count of  the number of questions to which anyone answered \"yes\"

    Argument
    answers_str -- answers from every group on the plane (your puzzle input)
    """
    answers = answers_str.split("\n\n")
    # # There are several ways to solve this in Python
    # # The following are ordered to explain the functioning of the final option
    # # for-loop
    # a0 = 0
    # for x in answers:
    #    a0 += len(set(x.replace("\n", "")))
    #
    # # This same can be express with reduce: reduce applies a function to x (rolling var) and y (element of list)
    # a1 = reduce(lambda x, y: x + len(set(y.replace("\n", ""))), answers, 0)
    #
    # # This same can be easier to understand by breaking it in map-reduce: map applies a function to every element and then reduce just makes the sum
    # a2 = reduce(lambda x, y: x + y, map(lambda x: len(set(x.replace("\n", ""))), answers))
    #
    # # In python sum can add the elements of a list so all we need is map to applies the function to every element and sum the resulting list
    # a3 = sum(map(lambda x: len(set(x.replace("\n", ""))), answers))
    #
    # # Instead of using map we can express the same with list comprehension and again use sum to add the elements
    return sum([len({*answer.replace("\n", "")}) for answer in answers])


def sum_count_of_everyone_yes(answers_str):
    """
    Sum of the count of the number of questions to which everyone answered \"yes\"

    Argument
    answers_str -- answers from every group on the plane (your puzzle input)
    """
    answers = answers_str.split("\n\n")
    # # Similarly to the previous problem
    # # This can be solved in different ways
    # b1 = reduce(
    #     lambda x, y: x
    #     + len(
    #         set(y.strip()).intersection(
    #             *list(map(lambda yy: set(yy), y.split("\n")))
    #         )
    #     ),
    #     data,
    #     0,
    # )
    return sum(
        [
            len({*y.strip()}.intersection(*[{*yy} for yy in y.split("\n")]))
            for y in answers
        ]
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Count the "yes" answers')
    parser.add_argument(
        "answers",
        type=open,
        help="answers from every group on the plane (your puzzle input) as txt file",
    )

    answers = parser.parse_args().answers
    answers_str = answers.read()
    answers.close()
    anyone_yes = sum_count_of_yes(answers_str)
    everyone_yes = sum_count_of_everyone_yes(answers_str)
    print(
        f'The sum fo the count of the number of questions to which anyone answered "yes" is {anyone_yes}'
    )
    print(
        f'The sum fo the count of the number of questions to which everyone answered "yes" is {everyone_yes}'
    )
