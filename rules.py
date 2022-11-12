import random
from helper_functions import count_dots


# Car acceleration rule
def rule_1(site, temp):
    """
    Given a velocity and number of free dots available in front, this rule
    decides if a car is allowed to accelerate by 1. Returns finals velocity
    """

    count = count_dots(site, temp)
    velocity = temp[site]

    if (int(velocity) < 5) and (count > int(velocity)):
        return int(velocity) + 1

    else:
        return int(velocity)


# Car deceleration rule
def rule_2(site, temp):
    """
    If car does not accelerate, then consider deceleration. Given a velocity
    and free dots available in front, this function determines if a car
    should decelerate
    """

    count = count_dots(site, temp)
    velocity = int(temp[site])
    j = count + 1
    if j <= int(velocity):
        velocity = j - 1
        return velocity
    else:
        return velocity


# Car probability deceleration rule
def rule_3(temp_velocity, probability):
    """
    Car has a given probability of reducing by 1
    """

    if temp_velocity == 0:
        pass
    else:
        random_probability = random.uniform(0, 1)

        if random_probability < probability:
            temp_velocity = int(temp_velocity) - 1
        else:
            pass
    return temp_velocity


# Car advancement rule
def rule_4(velocity, site, temp):
    """
    Advances cars by their velocities. This functions accounts for boundaries
    and returns the new site position
    """

    number_of_sites = len(temp)
    site_calculation = site

    for i in range(int(velocity)):

        if site >= (number_of_sites - 1):
            site_calculation = -1
            site = site_calculation

        if temp[site + 1] == ".":
            site_calculation = site_calculation + 1
            site = site_calculation

        elif temp[site + 1] == "G":
            site_calculation = site_calculation + 2
            site = site_calculation

    return site_calculation
