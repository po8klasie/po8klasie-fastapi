from geoalchemy2.shape import to_shape


def get_point_coords(geometry):
    shape = to_shape(geometry)
    return (shape.x, shape.y)
