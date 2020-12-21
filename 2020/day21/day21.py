#!/usr/bin/env python3

# --- Day 21: Allergen Assessment ---
# You reach the train's last stop and the closest you can get to your vacation island without getting wet. There aren't even any boats here, but nothing can stop you now: you build a raft. You just need a few days' worth of food for your journey.
# You don't speak the local language, so you can't read any ingredients lists. However, sometimes, allergens are listed in a language you do understand. You should be able to use this information to determine which ingredient contains which allergen and work out which foods are safe to take with you on your trip.
# You start by compiling a list of foods (your puzzle input), one food per line. Each line includes that food's ingredients list followed by some or all of the allergens the food contains.
# Each allergen is found in exactly one ingredient. Each ingredient contains zero or one allergen. Allergens aren't always marked; when they're listed (as in (contains nuts, shellfish) after an ingredients list), the ingredient that contains each listed allergen will be somewhere in the corresponding ingredients list. However, even if an allergen isn't listed, the ingredient that contains that allergen could still be present: maybe they forgot to label it, or maybe it was labeled in a language you don't know.
# For example, consider the following list of foods:
# mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
# trh fvjkl sbzzf mxmxvkd (contains dairy)
# sqjhc fvjkl (contains soy)
# sqjhc mxmxvkd sbzzf (contains fish)
# The first food in the list has four ingredients (written in a language you don't understand): mxmxvkd, kfcds, sqjhc, and nhms. While the food might contain other allergens, a few allergens the food definitely contains are listed afterward: dairy and fish.
# The first step is to determine which ingredients can't possibly contain any of the allergens in any food in your list. In the above example, none of the ingredients kfcds, nhms, sbzzf, or trh can contain an allergen. Counting the number of times any of these ingredients appear in any ingredients list produces 5: they all appear once each except sbzzf, which appears twice.
# Determine which ingredients cannot possibly contain any of the allergens in your list. How many times do any of those ingredients appear?
##
## Your puzzle answer was 2786.

# --- Part Two ---
# Now that you've isolated the inert ingredients, you should have enough information to figure out which ingredient contains which allergen.
# In the above example:
# mxmxvkd contains dairy.
# sqjhc contains fish.
# fvjkl contains soy.
# Arrange the ingredients alphabetically by their allergen and separate them by commas to produce your canonical dangerous ingredient list. (There should not be any spaces in your canonical dangerous ingredient list.) In the above example, this would be mxmxvkd,sqjhc,fvjkl.
# Time to stock your raft with supplies. What is your canonical dangerous ingredient list?
##
## prxmdlz,ncjv,knprxg,lxjtns,vzzz,clg,cxfz,qdfpq

import unittest
import re
from functools import reduce
from collections import OrderedDict


def parse_foods(food_list):
    regex = re.compile(r"(^.*) \(contains (.*)\)", re.MULTILINE)
    return regex.findall(food_list)


def allergens(foods):
    possible_allergens = {}
    for ingredients, allergens in foods:
        ingredients = set(ingredients.split(" "))
        for allergen in allergens.split(","):
            allergen = allergen.strip()
            if allergen in possible_allergens:
                possible_allergens[allergen] = possible_allergens[
                    allergen
                ].intersection(ingredients)
            else:
                possible_allergens[allergen] = ingredients
    return possible_allergens


def part_one(food_list):
    foods = parse_foods(food_list)
    possible_allergens = allergens(foods)
    all_ingredients = [
        ingredient for ingredients, _ in foods for ingredient in ingredients.split(" ")
    ]
    non_allergenic = set(all_ingredients)
    non_allergenic.difference_update(*possible_allergens.values())
    count_non_allergenic = reduce(
        lambda count, element: count + 1 if element in non_allergenic else count,
        all_ingredients,
        0,
    )
    return count_non_allergenic


def find_name(possible_allergens):
    for k, v in possible_allergens.items():
        if len(v) == 1:
            return k, v
    return None


def update_allergens(possible_allergens, remove):
    k, v = remove
    possible_allergens.pop(k)
    for k1, v1 in possible_allergens.items():
        possible_allergens[k1] = possible_allergens[k1] - v
    return possible_allergens


def find(possible_allergens):
    found_names = {}
    found = find_name(possible_allergens)
    while found != None:
        name, value = found
        found_names[name] = list(value)[0]
        possible_allergens = update_allergens(possible_allergens, remove=found)
        found = find_name(possible_allergens)
    return found_names


def part_two(food_list):
    foods = parse_foods(food_list)
    possible_allergens = allergens(foods)
    found_names = find(possible_allergens)
    ordered_allergens = OrderedDict(sorted(found_names.items()))
    ordered_allergens_values = ",".join([v for v in ordered_allergens.values()])
    return ordered_allergens_values


class TestDay21(unittest.TestCase):
    def test_part_one(self):
        example = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""
        self.assertEqual(part_one(example), 5)

    def test_part_two(self):
        example = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""
        self.assertEqual(part_two(example), "mxmxvkd,sqjhc,fvjkl")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Find allergens in food")
    parser.add_argument(
        "foods",
        type=open,
        help="A list of foods (your puzzle input), one food per line",
    )

    foods = parser.parse_args().foods
    foods_str = foods.read()
    foods.close()
    result = part_one(foods_str)
    print(f"{result} times non-allergenic ingredients appear")
    result = part_two(foods_str)
    print(result)
