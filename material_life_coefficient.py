import numpy as np

# Constantes
L_sun = 3.826e26  # Luminosidade solar (W)
F_earth = 1366    # Fluxo solar na Terra (W/m²)
au_to_m = 1.496e11  # 1 UA em metros
sigma = 0.2       # Largura da zona habitável
f_max = 12        # Frequência orbital máxima (ajustada)
R_star = 10       # Taxa de formação estelar
f_p = 1.0         # Fração de estrelas com planetas
n_e = 0.1         # Planetas por estrela
f_l = 0.1         # Vida surge
f_i = 0.015       # Vida inteligente (ajustada)
f_c = 0.1         # Comunicação
L_life = 1.5e-4   # Longevidade (ajustada)

def flux_factor(d, L_star):
    F = L_star / (4 * np.pi * (d * au_to_m)**2)
    F_norm = F / F_earth
    return np.exp(-((F_norm - 1)**2) / (2 * sigma**2))

def frequency_factor(f):
    return np.exp(-((f / f_max)**2))

def habitability_zone_factor(d, f, L_star):
    return flux_factor(d, L_star) * frequency_factor(f)

def kasting_factor(planet_type):
    types = {
        "1": (0.97, 0.97),  # Terra
        "2": (0.1, 0.01),   # Vênus
        "3": (0.3, 0.1),    # Marte
        "4": (0.7, 0.6),    # Kepler-452b
        "5": (0.5, 0.5)     # Outro
    }
    f_atm, f_agua = types.get(planet_type, (0.5, 0.5))
    return f_atm * f_agua

def habitability_coefficient(d, f, L_star, planet_type):
    f_HZ = habitability_zone_factor(d, f, L_star)
    n_eK = n_e * f_HZ
    H_K = kasting_factor(planet_type)
    D_bio = f_l * f_i * f_c
    C = (R_star * f_p * n_eK) * D_bio * L_life * H_K
    C_max = (R_star * f_p * n_e * 1.0) * D_bio * L_life * (1.0 * 1.0)
    return min(C / C_max, 1.0)

# Exemplos
examples = [
    ("Terra", 1.0, 1.0, L_sun, "1"),
    ("Vênus", 0.72, 1.63, L_sun, "2"),
    ("Marte", 1.52, 0.53, L_sun, "3"),
    ("Hot Jupiter", 0.05, 100, L_sun, "5"),
    ("Estrela fraca", 0.1, 36.5, 0.01 * L_sun, "5")
]
print("\nExemplos:")
for name, d, f, L_star, planet_type in examples:
    C = habitability_coefficient(d, f, L_star, planet_type)
    print(f"{name}: {C:.6f}")