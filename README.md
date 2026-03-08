# Python-Reporting-API-Program
Python Program with several API's for updating Google Sheets Reports

This used to be a program that i have created for the company that i have worked with so the reports are automated, hence some file and variable names are related to that.

The program runs from the main.py and opens a GUI with buttons for operations to choose from.

# Quantum Decoherence and Collision Models

This repository contains simulations of **Quantum Decoherence and Collision Models** that I developed as part of my Physics Engineering graduation project.

In this work, where we examine system-environment interactions, we model both memoryless (Markovian) and memory-environmental (Non-Markovian) quantum dynamics using the [QuTiP](https://qutip.org/) library in Python.

## 📂 Contents and Simulations

### 1. `Markovian_Analytical vs Collision Model.ipynb`

This file contains a simulation of **Markovian (Memoryless)** dynamics through a collision model.

- The environment (Ancilla) is included in the system in each collision in a "fresh" and "cold" ground state ($|0\rangle$). - An **Amplitude Damping** interaction simulating energy exchange has been established.
- The numerical coherence loss data obtained from the Collision Model is plotted comparatively with the analytical solution, the $\cos(g\tau)^n$ function.

### 2. `non_markov_strategies.ipynb`
This simulation examines a more complex structure where **Non-Markovian (Memory)** strategies are integrated into the system. - A **memory effect** is created in the system by establishing an interaction ($U_{AA}$) based on SWAP operators between successive ancillaries forming the environment.
- Memory power can be dynamically controlled with the $\theta$ parameter ($\theta = 0$ Markovian, $\theta = \pi/2$ Full Swap, $\theta = \pi/4$ Maximum Entanglement). - Time evolution was designed by taking the exponent from the Hamiltonian, ensuring that the matrix remains "Unitary" (probability-preserving).

**"Coherence Revival"** effects, where the information/energy lost by the system to the environment is returned to the system, have been successfully observed. ## 🛠️ Technologies Used
- **Python 3.x**
- **QuTiP** (Quantum Toolbox in Python)
- **NumPy** (Physical parameters and matrix operations)
- **Matplotlib** (Visualization of superposition/coherence and trace graphs)
