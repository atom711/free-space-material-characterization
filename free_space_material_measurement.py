import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. SETUP LAB CONSTANTS & FREQUENCY SWEEP
# ==========================================
freqs = np.linspace(8e9, 18e9, 1000)  # Sweep from 8 GHz to 18 GHz
c0 = 3e8                               # Speed of light in vacuum (m/s)
z0 = 377.0                             # Intrinsic impedance of free space (Ohms)

# ==========================================
# 2. DEFINE MATERIAL PARAMETERS (Radome Panel)
# ==========================================
epsilon_prime = 4.5    # Permittivity (energy storage/dielectric constant)
loss_tangent = 0.02    # Material loss tangent (tan delta)
epsilon_double_prime = epsilon_prime * loss_tangent

# Complex Permittivity: e* = e' - j*e''
epsilon_complex = complex(epsilon_prime, -epsilon_double_prime)
mu_complex = complex(1.0, 0.0)  # Non-magnetic material

# Calculate Material Intrinsic Impedance: Z = sqrt(mu / epsilon)
z_material = z0 * np.sqrt(mu_complex / epsilon_complex)

# Define physical sample thickness: 6 millimeters (0.006 meters)
d = 0.006 

# ==========================================
# 3. MATHEMATICAL WAVE PROPAGATION MODEL
# ==========================================
s11_list = []
s21_list = []

for f in freqs:
    # Free space wavenumber and material wavenumber
    k0 = (2 * np.pi * f) / c0
    km = k0 * np.sqrt(epsilon_complex * mu_complex)
    
    # Half-space reflection coefficient (air-to-material boundary)
    gamma = (z_material - z0) / (z_material + z0)
    
    # Phase propagation factor through thickness 'd'
    # Uses Euler's formula to handle spatial rotation
    P = np.exp(-1j * km * d)
    
    # Air-Line/Free-Space S-Parameter Extraction Formulas
    # Accounts for infinite internal reflections inside the material sample
    s11_denom = 1 - (gamma**2) * (P**2)
    s11 = (gamma * (1 - P**2)) / s11_denom
    s21 = (P * (1 - gamma**2)) / s11_denom
    
    s11_list.append(s11)
    s21_list.append(s21)

s11_array = np.array(s11_list)
s21_array = np.array(s21_list)

# ==========================================
# 4. PLOT 1: STANDARD S-PARAMETER MAGNITUDE
# ==========================================
# ==========================================
# 4. PLOT 1: SEPARATE MAGNITUDE SWEEP
# ==========================================
plt.figure(figsize=(7, 5)) # Independent standard rectangular canvas
plt.plot(freqs / 1e9, 20 * np.log10(np.abs(s11_array)), label='$S_{11}$ (Reflection)', color='crimson', lw=2)
plt.plot(freqs / 1e9, 20 * np.log10(np.abs(s21_array)), label='$S_{21}$ (Transmission)', color='dodgerblue', lw=2)
plt.title('VNA Material Measurement Sweep')
plt.xlabel('Frequency (GHz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True, linestyle='--')
plt.legend()
plt.tight_layout()

# Save directly to your report directory
plt.savefig('lab_materials_magnitude.png', dpi=300)
plt.close() # Closes the canvas to free system resources

# ==========================================
# 5. PLOT 2: SEPARATE POLAR PHASE SPACE
# ==========================================
plt.figure(figsize=(6, 6)) # Square canvas optimized for polar grids
ax = plt.subplot(1, 1, 1, projection='polar') # Standalone polar configuration
ax.plot(np.angle(s11_array), np.abs(s11_array), label='$S_{11}$ Trace', color='crimson', lw=2)
ax.set_rmax(1.0)  
ax.set_rticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_title("S11 Complex Phase Trajectory", va='bottom')
ax.grid(True)
ax.legend()
plt.tight_layout()

# Save directly to your report directory
plt.savefig('lab_materials_polar.png', dpi=300)
plt.close()

# ==========================================
# 4. COMPOSITE S-PARAMETER ANALYSIS LAYOUT
# ==========================================
fig = plt.figure(figsize=(10, 8))

# Subplot 1: Standard Magnitude Sweep (Spans top row)
ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)
ax1.plot(freqs / 1e9, 20 * np.log10(np.abs(s11_array)), label='$S_{11}$ (Reflection)', color='crimson', lw=2)
ax1.plot(freqs / 1e9, 20 * np.log10(np.abs(s21_array)), label='$S_{21}$ (Transmission)', color='dodgerblue', lw=2)
ax1.set_title('VNA Bulk Material Measurement Analysis', fontsize=12, fontweight='bold')
ax1.set_ylabel('Magnitude (dB)', fontweight='bold')
ax1.set_xlabel('Frequency (GHz)', fontweight='bold')
ax1.set_ylim(-35, 2)
ax1.grid(True, linestyle='--')
ax1.legend(loc='lower left')

# Subplot 2: Linear Transmission Phase Sweep (Bottom Left)
ax2 = plt.subplot2grid((2, 2), (1, 0))
ax2.plot(freqs / 1e9, np.degrees(np.unwrap(np.angle(s21_array))), label='$S_{21}$ Phase', color='crimson', lw=2)
ax2.set_title('$S_{21}$ Phase Accumulation', fontsize=10, fontweight='bold')
ax2.set_xlabel('Frequency (GHz)', fontweight='bold')
ax2.set_ylabel('Phase (degrees)', fontweight='bold')
ax2.grid(True, linestyle='--')
ax2.legend(loc='lower left')

# Subplot 3: Complex Polar Trajectory Mapping (Bottom Right)
ax3 = plt.subplot2grid((2, 2), (1, 1), projection='polar')
ax3.plot(np.angle(s11_array), np.abs(s11_array), label='$S_{11}$ Trace', color='crimson', lw=2)
ax3.set_rmax(1.0)  
ax3.set_rticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax3.set_title("$S_{11}$ Complex Phase Trajectory", va='bottom', fontsize=10, fontweight='bold')
ax3.grid(True)
ax.legend(loc="upper left")

plt.tight_layout()

# Save composite canvas directly to your report directory
plt.savefig('lab_materials_composite_analysis.png', dpi=300)
plt.close()