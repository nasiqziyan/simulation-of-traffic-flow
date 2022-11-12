# -*- coding: utf-8 -*-
"""
Created on Tue Apr 7 13:30:29 2020
"""

# -*- coding: utf-8 -*-

import light_profiles
import rules
import numpy as np
import matplotlib.pyplot as plt
import helper_functions as hf


def generate_road(density, number_of_sites, traffic_light_density, chosen_light_profile, unit_phase, seconds):
    """
    Main function:
    Takes in raw variables and runs helper functions / rules to evolve the car
    positions over a fixed time (seconds)
    """

    flow_counter = 0

    verified_array = hf.verify_array(
        hf.create_initial_array(density,
                                number_of_sites,
                                traffic_light_density,
                                chosen_light_profile,
                                unit_phase))

    number_of_lights = round(traffic_light_density * number_of_sites)
    number_of_sites_with_lights = round(number_of_sites + number_of_lights)
    traffic_light_positions = hf.light_positions(number_of_sites_with_lights, number_of_lights)
    phase_array = hf.calculate_phase_array(number_of_lights, chosen_light_profile, unit_phase)

    # Timestep is updated continuously; new versions aren't created.
    timestep = np.copy(verified_array)

    # selected_function = [k for k, v in graphing_functions.items() if v][0]

    # Prints a block of <seconds> lines. If seconds = 10, 10 lines are printed to file.
    for second in range(seconds):

        # Ensures that update_traffic_lights runs only once every second.
        # False: Lights unchanged; hasn't run
        # True : Lights changed; has run
        guard_condition = False

        site = 0

        print(np.array2string(timestep, separator='', formatter={'str_kind': lambda x: x}))

        # New versions of temp created every second
        temp = np.copy(timestep)

        # Iterate through sites
        while site < len(verified_array):

            # until you reach a number (car with velocity equal to number)
            if temp[site] in [".", "G", "R"]:
                site = site + 1

            else:

                original_velocity = temp[site]

                # Immediately advance car positions without applying any other rules
                new_site = rules.rule_4(original_velocity, site, temp)

                if new_site < site:
                    flow_counter = flow_counter + 1

                timestep[site] = "."
                timestep[new_site] = original_velocity

                if not guard_condition:
                    hf.update_traffic_lights(timestep,
                                             traffic_light_positions,
                                             phase_array,
                                             number_of_lights,
                                             chosen_light_profile)

                    guard_condition = True

                # Position correct at this point, but velocity incorrect.
                # Therefore, apply rule_1 (acceleration).
                temp_velocity = rules.rule_1(new_site, timestep)

                # If acceleration doesn't occur, consider deceleration
                if int(original_velocity) == int(temp_velocity):
                    temp_velocity = rules.rule_2(new_site, timestep)

                # Apply rule_3 (probability)
                temp_velocity = rules.rule_3(temp_velocity, 0.3)

                final_velocity = temp_velocity

                # Velocity and position all correct
                timestep[new_site] = final_velocity

                site = site + 1

    flow_rate = flow_counter / seconds

    return flow_rate


def flow_array_graph(seconds):
    density_array = np.arange(0.04, 0.82, 0.01)
    mean_flow_array = []
    std_dev_array = []

    # assigning dummy value to flow_array to fix warning:
    # Local variable 'flow_array' might be referenced before assignment
    flow_array = '_'

    for density in density_array:

        flow_array = []

        for j in range(50):
            flow_rate = generate_road(float(density), 64, 4 / 64, light_profiles.light_pro_2, 0, seconds)
            flow_array.append(flow_rate)

        mean_value = np.mean(flow_array)
        mean_flow_array.append(mean_value)
        std_dev = np.std(flow_array)
        std_dev_array.append(std_dev)

    np.array(flow_array)
    np.array(mean_flow_array)
    np.array(std_dev_array)

    plt.plot(np.arange(0.04, 0.82, 0.01), mean_flow_array)
    plt.errorbar(density_array, mean_flow_array, yerr=std_dev_array, fmt='.', c='blue')
    plt.xlabel("Vehicular Density (vehicles per cell)")
    plt.ylabel("Mean flow rate (vehicles per timestep)")
    plt.show()

    return mean_flow_array, std_dev_array


def phase_flow_graph(density_constant, seconds):
    unit_phase_range = np.arange(0, 1, 0.01)

    mean_flow_array = []
    std_dev_array = []

    # assigning dummy value to flow_array to fix warning:
    # Local variable 'flow_array' might be referenced before assignment
    flow_array = '_'

    for phase in unit_phase_range:

        flow_array = []

        for j in range(50):
            flow_rate = generate_road(float(density_constant),
                                      64,
                                      4 / 64,
                                      light_profiles.light_profile_balanced,
                                      phase,
                                      seconds)

            flow_array.append(flow_rate)

        mean_value = np.mean(flow_array)
        mean_flow_array.append(mean_value)
        std_dev = np.std(flow_array)
        std_dev_array.append(std_dev)

    np.array(flow_array)
    mean_flow_array = np.array(mean_flow_array)
    std_dev_array = np.array(std_dev_array)

    plt.plot(unit_phase_range, mean_flow_array)
    plt.errorbar(unit_phase_range, mean_flow_array, yerr=std_dev_array, fmt='o', label="", c='blue')
    plt.xlabel("Phase")
    plt.ylabel("Mean flow rate (vehicles per timestep)")
    plt.show()

    return mean_flow_array, std_dev_array


def vary_no_of_lights_graph(density, seconds):
    light_no_range = np.arange(1, 25, 1)

    mean_flow_array = []
    std_dev_array = []

    # assigning dummy value to flow_array to fix warning:
    # Local variable 'flow_array' might be referenced before assignment
    flow_array = '_'

    for i in light_no_range:

        flow_array = []

        for j in range(100):
            flow_rate = generate_road(float(density), 64, (int(i) * 1 / 64), light_profiles.light_pro_2, 0, seconds)
            flow_array.append(flow_rate)

        mean_value = np.mean(flow_array)
        mean_flow_array.append(mean_value)
        std_dev = np.std(flow_array)
        std_dev_array.append(std_dev)

    np.array(flow_array)
    mean_flow_array = np.array(mean_flow_array)
    std_dev_array = np.array(std_dev_array)

    plt.plot(light_no_range, mean_flow_array)
    plt.errorbar(light_no_range, mean_flow_array, yerr=std_dev_array, fmt='o', label="", c='blue')
    plt.xlabel("Number of Traffic Lights")
    plt.ylabel("Mean flow rate (vehicles per timestep)")
    plt.show()

    return mean_flow_array, std_dev_array


def average_flow_graph(density, seconds):
    mean_flow_array = []
    std_dev_array = []

    internal_range_values = np.array([1, 2, 3, 4, 6, 12])

    profiles = np.array([light_profiles.light_pro_1,
                         light_profiles.light_pro_2,
                         light_profiles.light_pro_3,
                         light_profiles.light_pro_4,
                         light_profiles.light_pro_6,
                         light_profiles.light_pro_12])

    for profile in profiles:
        flow_array = []

        for j in range(100):
            flow_rate = generate_road(density, 64, 4 / 64, profile, 0, seconds)
            flow_array.append(flow_rate)

        mean_value = np.mean(flow_array)
        mean_flow_array.append(mean_value)
        std_dev = np.std(flow_array)
        std_dev_array.append(std_dev)

    np.array(mean_flow_array)
    np.array(std_dev_array)

    plt.errorbar(internal_range_values, mean_flow_array, yerr=std_dev_array, fmt='.', c='blue')
    plt.xlabel("Light Profile, i (light_profile_i)")
    plt.ylabel("Mean flow rate (vehicles per timestep)")
    plt.show()

    return mean_flow_array, std_dev_array


graphing_functions = {
    'flow_array_graph': False,
    'phase_flow_graph': False,
    'vary_no_of_lights_graph': False,
    'average_flow_graph': False
}

mean_flow_array_result, std_dev_flow_array_result = flow_array_graph(seconds=10)

mean_flow_array_phase, std_dev_flow_array_phase = phase_flow_graph(density_constant=0.15, seconds=10)

vary_lights_mean_array, vary_lights_std_dev_array = vary_no_of_lights_graph(density=0.4, seconds=10)

average_flow_array, average_flow_std_array = average_flow_graph(0.2, seconds=10)
