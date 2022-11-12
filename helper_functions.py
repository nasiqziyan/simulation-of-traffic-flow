import random
import numpy as np


def light_positions(number_of_sites, number_of_lights):
    """
    Takes the updated number of sites and determines the positions
    of the traffic lights and returns it as an array.
    """

    spacing = int(number_of_sites / number_of_lights)
    initial_phase = int(spacing / 2)
    spacing_integer_multiples = []

    for i in range(number_of_lights):
        spacing_integer_multiples.append((i*spacing)+initial_phase)

    light_positions_array = np.array(spacing_integer_multiples)

    return light_positions_array


def create_initial_array(density, number_of_sites, traffic_light_density, light_profile, unit_phase):
    """
    density [float] {0,1}:
    number_of_sites [int]:
    traffic_light_density [float] {0,1}
    light_profile [array] of length 24: An array of R's and G's. Traffic lights start at a given
                                        position in light profile and move to next element every
                                        second

    unit_phase [float] {0,1}:           When unit_phase is 0, all lights start at the same position
                                        in light profile (coherent). When unit_phase is 1, the initial
                                        positions of traffic_lights in the light_profile are equally
                                        spaced.

    """
    number_of_cars = round(number_of_sites * density)

    # 1 refers to number of rows; [0] since array encapsulated in larger array.

    array = np.full((1, number_of_sites), ".")[0]

    number_of_lights = round(traffic_light_density * number_of_sites)

    # Elements (traffic_lights) added to original array to ensure number_of_sites is unchanged.

    number_of_sites_with_lights = number_of_sites + number_of_lights

    array = np.append(array, number_of_lights * ["."])

    traffic_light_positions = light_positions(number_of_sites_with_lights,
                                              number_of_lights)

    # Creates an array of numbers which exclude those numbers found in light_positions

    allowed_car_positions = [i for i in range(0, number_of_sites_with_lights)
                             if not (i in traffic_light_positions)]

    # Numbers are sampled from to find car_positions

    final_car_positions = random.sample(allowed_car_positions, number_of_cars)

    phase_array = calculate_phase_array(number_of_lights, light_profile, unit_phase)

    # Replacing positions in array with traffic lights

    for i in range(number_of_lights):
        array[int(traffic_light_positions[i])] = light_profile[int(phase_array[i])]

    for i in final_car_positions:
        # Sets cars' velocity
        array[i] = random.randint(0, 5)

    return array


def calculate_phase_array(number_of_lights, light_profile, unit_phase):

    phase_array = []

    # Largest spacing between two adjacent lights in light_profile for all lights to be equidistant.

    max_phase = len(light_profile) / number_of_lights

    # determined spacings between light positions in the profile using unit_phase.

    phase_proportion = max_phase * unit_phase

    for i in range(number_of_lights):
        number = round(i * phase_proportion)

        # Phase array represents the positions of the lights in the light_profile.

        phase_array.append(number)

    phase_array = np.array(phase_array)

    return phase_array


def count_dots(site, initial_array):
    """
    This functions counts the number of dots between two adjacent cars or
    between a car and a red traffic light. When counting across a green light,
    the green light isn't counted as a dot.
    Note: Red lights aren't counted as dots either
    """

    # counts the dots between two cars
    counter = 0

    while True:
        if site + 1 >= len(initial_array):
            site = -1
            # because we want the next pos to be at 0th pos
        else:
            pass

        if initial_array[site + 1] == '.':
            counter = counter + 1
            site = site + 1

        elif initial_array[site + 1] == 'G':
            site = site + 1

        elif initial_array[site + 1] == 'R':
            return counter

        else:

            return counter


def verify_array(initial_array):
    """
    Takes the initial array and changes the velocities of cars to avoid
    violations of the rules (rule_1-rule_4) and traffic light violations
    """

    site = 0

    while site < len(initial_array):

        if initial_array[site] in [".", "G", "R"]:
            site = site + 1

        else:

            count = count_dots(site, initial_array)

            # setting the velocity to an allowed velocity
            if count >= 5:
                pass

            else:
                initial_array[site] = count

            site = site + 1

    return initial_array


def update_traffic_lights(timestep, traffic_light_positions, phase_array, number_of_lights, chosen_light_profile):

    for i in range(number_of_lights):
        if (phase_array[i] + 1) >= 24:
            phase_array[i] = -1

        phase_array[i] = phase_array[i] + 1

        timestep[int(traffic_light_positions[i])] = chosen_light_profile[int(phase_array[i])]