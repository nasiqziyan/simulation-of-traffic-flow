import numpy as np

def flow_array_1(seconds):

    density_array = np.arange(0.04, 0.82, 0.01)
    mean_flow_array = []
    std_dev_array = []

    # assigning dummy value to flow_array to fix warning:
    # Local variable 'flow_array' might be referenced before assignment
    flow_array = '_'

    for density in density_array:

        flow_array = []

        for j in range(50):
            flow_array_1_called = True
            flow_rate = position(float(density), 64, 4/64, light_profiles.light_pro_2, 0, seconds)
            flow_array.append(flow_rate)
            flow_array_1_called = False


        mean_value = np.mean(flow_array)
        mean_flow_array.append(mean_value)
        std_dev = np.std(flow_array)
        std_dev_array.append(std_dev)

    np.array(flow_array)
    np.array(mean_flow_array)
    np.array(std_dev_array)

    plt.plot(np.arange(0.04, 0.82, 0.01), mean_flow_array)
    plt.errorbar(density_array, mean_flow_array, yerr=std_dev_array, fmt='.', c='blue')
    plt.show()

    return mean_flow_array, std_dev_array