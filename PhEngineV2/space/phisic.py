import glm

G = 6.67430e-11  # the gravitational constant


def calculate_gravitational_force(
        pos1: glm.vec2, pos2: glm.vec2,
        mass1: float, mass2: float
) -> tuple[float]:
    """ calculation of the vector of gravitational interaction of 2 bodies """
    if pos1 == pos2:
        return glm.vec2(0)
    
    distance_vector: glm.vec2 = pos2 - pos1
    distance: float = glm.distance(pos1, pos2)
    
    force_magnitude: float = (G*mass1*mass2)/distance**2
    force_direction: float = glm.atan(distance_vector.y, distance_vector.x)
    
    force_vector: glm.vec2 = glm.vec2(
        force_magnitude*glm.cos(force_direction),
        force_magnitude*glm.sin(force_direction)
    )
    return force_vector
