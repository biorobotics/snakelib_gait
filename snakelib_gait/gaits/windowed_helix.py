import numpy as np

from .compound_serpenoid import compound_serpenoid


def windowed_helix(
    phase:float,
    n_modules:float,
    window_n:int,
    bend_angle:float,
    module_length:float,
    radius:float,
    pitch:float,
    time_frequency:float,
):
    """Calculate joint angles for manual helical rolling.

    Args:
        phase:
            Abstract time value that lets us set where we are in the gait cycle
            for the two helixes.
        n_modules:
            Number of modules in the snake.
        window_n:
            Where along the snake the gait changes from a->b, expressed in
            number of modules.
        bend_angle:
            The bend between the two helixes in radians. For a T-junction this
            would be pi/2 or -pi/2 depending on the direction we want to go
        module_length:
            Distance between one joint and the next.
        radius:
            Radius of helix. Same unit as module_length.
        pitch:
            Axial distance between modules after one rotation. Same unit as
            module_length.
        time_frequency:
            How many times the snake rolls per 1 phase
    """
    # Convert to pitch per radian
    p = pitch / (radius * 2 * np.pi)
    # angle = np.arctan2(pitch, 1)
    # print(angle)
    spatial_frequency = (module_length * p) / (p**2 + radius**2)
    amplitude = (2 * radius) / p * np.sin(spatial_frequency)
    # Back helix is identical to normal helix
    helix_a = compound_serpenoid(
        phase, n_modules,
        offsets=[0, 0],
        amplitudes=[amplitude] * 2,
        spatial_frequencies=[spatial_frequency] * 2,
        time_frequencies=[time_frequency] * 2,
        phase_shift=0.25
    )
    # Front helix is offset in phase to produce bend.
    phase_offset = bend_angle * np.sign(amplitude * spatial_frequency)
    # Phase is normalized from 0-1 and also depends on time frequency
    phase_offset /=  2 * np.pi * time_frequency
    helix_b = compound_serpenoid(
        phase - phase_offset, n_modules,
        offsets=[0, 0],
        amplitudes=[amplitude] * 2,
        spatial_frequencies=[spatial_frequency] * 2,
        time_frequencies=[time_frequency] * 2,
        phase_shift=0.25
    )
    # Apply window
    mask = np.array([i >= window_n for i in range(n_modules)])
    # if window_n > 0 and window_n < n_modules:
    #     mask[int(window_n)] = window_n % (int(window_n) + 1)
    return helix_a * mask + helix_b * (1-mask)
