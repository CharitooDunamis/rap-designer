try:
    from rpm.rpm_functions import *
except (ImportError, SystemError) as e:
    pass

sample_height = None
sample_diameter = None
sample_density = 0.0275
deposit_depth = 300   # overburden height
unicomp_strength = 100
initial_room_width = None
max_pillar_strength = None
factor_of_safety_value = None
angle_of_friction = None
cohesion = 56
bearing_capacity_value = None

SALAMON_MUNRO_G = 62
SALAMON_MUNRO_T = 0.46
SALAMON_MUNRO_R = -0.66

# pillar_strength = salamon(sample_diameter, sample_height)
#
# pre_stress = pre_mining_field_stress(sample_density, deposit_depth)
#
# pillar_stress = square_pillar_stress(pre_stress, initial_room_width, sample_diameter)
#
# fos = factor_of_safety(pillar_strength, pillar_stress)
#
# if fos >= factor_of_safety_value:
#     pass
# else:
#     pass

if __name__ == "__main__":
    pass
