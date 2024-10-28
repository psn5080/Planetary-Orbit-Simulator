# Planet Simulation

This project is a simulation of the solar system using Pygame. It models the gravitational interactions between planets and allows users to control the simulation through various actions such as zooming, panning, and adjusting the simulation speed.

## Features

- Realistic gravitational interactions between planets
- Adjustable simulation speed
- Zoom and pan functionality
- Display of planetary orbits
- Display of simulation time, total energy, number of planets, average velocity, and energy accuracy
- Pause and resume functionality

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/planet-simulation.git
    cd planet-simulation
    ```

2. **Install the required dependencies:**

    ```sh
    pip install pygame
    ```

## Usage

1. **Run the simulation:**

    ```sh
    python simulator.py
    ```

2. **Controls:**

    - **Speed Up:** Increases the simulation speed.
    - **Slow Down:** Decreases the simulation speed.
    - **Zoom In:** Zooms into the simulation.
    - **Zoom Out:** Zooms out of the simulation.
    - **Pan Left:** Pans the view to the left.
    - **Pan Right:** Pans the view to the right.
    - **Pause/Resume:** Pauses or resumes the simulation.
    - **Reset View:** Resets the zoom and pan to the default view.
    - **Toggle Orbits:** Toggles the display of planetary orbits.

3. **Mouse Controls:**

    - **Left Mouse Button:** Click and drag to pan the view.
    - **Mouse Wheel Up:** Zoom in.
    - **Mouse Wheel Down:** Zoom out.

## Code Structure

- **`simulator.py`**: Main file containing the simulation logic and Pygame setup.
- **`Planet` class**: Represents a planet with properties such as position, velocity, mass, and methods for drawing, updating position, and calculating energies.
- **`Button` class**: Represents a UI button with properties for position, size, text, and action.

## Key Functions

- **`main()`**: Initializes the simulation, sets up the planets and buttons, and contains the main loop for the simulation.
- **`change_time_scale(factor, state)`**: Adjusts the simulation speed.
- **`change_zoom_scale(factor, state)`**: Adjusts the zoom level.
- **`change_pan(dx, dy, state)`**: Adjusts the pan position.
- **`toggle_pause(state)`**: Pauses or resumes the simulation.
- **`reset_view(state)`**: Resets the zoom and pan to the default view.
- **`toggle_orbits(state)`**: Toggles the display of planetary orbits.
- **`calculate_total_energy(planets)`**: Calculates the total kinetic and potential energy of the system.
- **`calculate_average_velocity(planets)`**: Calculates the average velocity of all planets.

## Dependencies

- **Pygame**: Used for rendering the simulation and handling user input.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This project was inspired by the beauty and complexity of our solar system.
- Special thanks to the Pygame community for their excellent documentation and support.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For any questions or suggestions, please open an issue or contact me at buzzpranav06@gmail.com](mailto:buzzpranav06@gmail.com).