import random
from math import sqrt


def change_netlist_order(chip, order_choice):
    """
    Function changing the order of the connections that have to be made by the algorithm.

    Returns:
        wire_connections : the sorted connections between the gates for this chip.
    """
    if order_choice == "random":
        wire_connections = change_order_random(chip)
        return wire_connections

    elif order_choice == "reverse":
        wire_connections = change_order_reverse(chip)
        return wire_connections

    elif order_choice == "short":
        wire_connections = change_order_distance(chip, reverse=False)
        return wire_connections

    elif order_choice == "long":
        wire_connections = change_order_distance(chip, reverse=True)
        return wire_connections

    elif order_choice == "least-connections":
        wire_connections = change_order_number_of_connections(chip, reverse=False)
        return wire_connections

    elif order_choice == "most-connections":
        wire_connections = change_order_number_of_connections(chip, reverse= True)
        return wire_connections

    elif order_choice == "sum-lowest":
        wire_connections = change_order_sum(chip, reverse=False)
        return wire_connections

    elif order_choice == "sum-highest":
        wire_connections = change_order_sum(chip, reverse=True)
        return wire_connections

    elif order_choice == "middle":
        wire_connections = change_order_middle_to_outside(chip, reverse=False)
        return wire_connections

    elif order_choice == "outside":
        wire_connections = change_order_middle_to_outside(chip, reverse=True)
        return wire_connections

    elif order_choice == "intra-quadrant":
        wire_connections = change_order_quadrant(chip, reverse=False)
        return wire_connections

    elif order_choice == "inter-quadrant":
        wire_connections = change_order_quadrant(chip, reverse=True)
        return wire_connections

    # if none of these applied, just use the basic sorting (not sorting)
    else:
        wire_connections = chip.wire_connections
        return wire_connections


def change_order_random(chip):
    """
    Function that sorts the wire connections randomly

    Args:
        chip (chip): the current chip that we are working on

    Returns:
        wire_connections: the sorted wire connections between the gates on this chip
    """

    wire_connections = chip.wire_connections
    random.shuffle(wire_connections)

    return wire_connections


def change_order_reverse(chip):
    """
    Function that sorts the wire connections in reverse order.

    Args:
        chip (chip): the current chip that we are working on

    Returns:
        wire_connections: the sorted wire connections between the gates on this chip
    """
    wire_connections = chip.wire_connections

    wire_connections.reverse()

    return wire_connections


def change_order_distance(chip, reverse):
    """
    Function that sorts the wire connections from the shortest to longest distance between the two gates.

    Args:
        chip (chip): the current chip that we are working on

    Returns:
        wire_connections: the sorted wire connections between the gates on this chip
    """
    wire_connections = chip.wire_connections

    wire_connections.sort(key=lambda connection: calculate_distance(connection, chip), reverse=reverse)

    return wire_connections


def calculate_distance(connection, chip):
    """
    function to calculate the distance between the two given gates for the wire connection

    Args:
        connection (wire_connection): the connection between the two gates
        chip (chip): the current chip that we are working on

    Returns:
        distance: distance from gate a to gate b
    """

    # get the first gate's location
    gate_a_id = connection[0]
    gate_a = chip.gates[gate_a_id]
    a_location = gate_a.location

    # get the second gate's location
    gate_b_id = connection[1]
    gate_b = chip.gates[gate_b_id]
    b_location = gate_b.location

    distance = sqrt((a_location.x - b_location.x) ** 2 + (a_location.y - b_location.y) ** 2)

    return distance


def change_order_number_of_connections(chip, reverse):
    """
    Function that sorts the wire connections based on the amount of connections one of the two (highest) gates has with other gates.
    In this case from most to least connections.

    Args:
        chip (chip): the current chip that we are working on

    Returns:
        wire_connections: the sorted wire connections between the gates on this chip
    """
    wire_connections = chip.wire_connections

    # Create a dictionary to store the connection count for each gate
    connection_count = {}

    # Count the connections for each gate
    for connection in wire_connections:
        gate_a_id, gate_b_id = connection

        # Count connections for gate A
        connection_count[gate_a_id] = connection_count.get(gate_a_id, 0) + 1

        # Count connections for gate B
        connection_count[gate_b_id] = connection_count.get(gate_b_id, 0) + 1

    # Sort wire_connections based on the number of connections for the gates
    wire_connections.sort(key=lambda connection: max(connection_count[connection[0]], connection_count[connection[1]]), reverse=reverse)

    return wire_connections


def change_order_sum(chip, reverse):
    """
    Function that sorts the wire connections based on the amount of connections both of the gates have combined.
    Reverse True means it should sort from highest to lowest and False means lowest to highest.

    Args:
        chip (chip): the current chip that we are working on

    Returns:
        wire_connections: the sorted wire connections between the gates on this chip
    """
    wire_connections = chip.wire_connections

    # Create a dictionary to store the connection count for each gate
    connection_count = {}

    # Count the connections for each gate
    for connection in wire_connections:
        gate_a_id, gate_b_id = connection

        # Count connections for gate A
        connection_count[gate_a_id] = connection_count.get(gate_a_id, 0) + 1

        # Count connections for gate B
        connection_count[gate_b_id] = connection_count.get(gate_b_id, 0) + 1

    # Sort wire_connections based on the sum of connection counts for both gates in reverse order
    wire_connections.sort(key=lambda connection: connection_count[connection[0]] + connection_count[connection[1]], reverse=reverse)

    return wire_connections


def change_order_middle_to_outside(chip, reverse):
    """
    Function that sorts the wire connections based on their proximity to the middle of the chip,
    from closest to the middle to the most outside in case reverse is False, and from outside to the middle in case it is True.

    Args:
        chip (chip): the current chip that we are working on

    Returns:
        wire_connections: the sorted wire connections between the gates on this chip
    """
    wire_connections = chip.wire_connections

    # Calculate the coordinates of the middle of the chip
    middle_x = chip.grid.width / 2
    middle_y = chip.grid.height / 2

    # Sort wire_connections based on the distance from the middle to each gate involved in the connection
    wire_connections.sort(key=lambda connection: calculate_distance_to_middle(connection, chip, middle_x, middle_y), reverse=reverse)

    return wire_connections


def calculate_distance_to_middle(connection, chip, middle_x, middle_y):
    """
    Function to calculate the distance between the middle of the chip and the gates involved in the wire connection.

    Args:
        connection (wire_connection): the connection between the two gates
        chip (chip): the current chip that we are working on
        middle_x (float): x-coordinate of the middle of the chip
        middle_y (float): y-coordinate of the middle of the chip

    Returns:
        distance: distance from the middle of the chip to the gates involved in the connection
    """
    # Get the locations of the gates involved in the connection
    gate_a_id, gate_b_id = connection
    gate_a = chip.gates[gate_a_id]
    gate_b = chip.gates[gate_b_id]

    # Calculate the distances from each gate to the middle of the chip
    distance_a = sqrt((gate_a.location.x - middle_x) ** 2 + (gate_a.location.y - middle_y) ** 2)
    distance_b = sqrt((gate_b.location.x - middle_x) ** 2 + (gate_b.location.y - middle_y) ** 2)

    # Return the maximum distance among the gates involved in the connection
    return max(distance_a, distance_b)


def change_order_quadrant(chip, reverse):
    """
    Function that sorts the wire connections by dividing the chip into quadrants and sorting connections within the same
    quadrant first, followed by connections between gates in different quadrants.

    Args:
        chip (chip): the current chip that we are working on

    Returns:
        wire_connections: the sorted wire connections between the gates on this chip
    """
    wire_connections = chip.wire_connections

    # Divide the chip into quadrants based on the center point
    center_x = chip.grid.width / 2
    center_y = chip.grid.height / 2

    # Sort wire connections by quadrant first, and then by distance within each quadrant
    wire_connections.sort(key=lambda connection: (
        is_same_quadrant(connection, chip, center_x, center_y),
        -calculate_distance(connection, chip)  # negate the distance to sort in reverse order within the quadrant
    ), reverse=reverse)

    return wire_connections


def is_same_quadrant(connection, chip, center_x, center_y):
    """
    Function to check if the gates in a connection belong to the same quadrant.

    Args:
        connection (wire_connection): the connection between two gates
        chip (chip): the current chip that we are working on
        center_x (float): the x-coordinate of the center point
        center_y (float): the y-coordinate of the center point

    Returns:
        bool: True if the gates are in the same quadrant, False otherwise
    """
    gate_a_id, gate_b_id = connection

    # Get the quadrant indices for the gates
    quadrant_a = get_quadrant_index(chip.gates[gate_a_id].location, center_x, center_y)
    quadrant_b = get_quadrant_index(chip.gates[gate_b_id].location, center_x, center_y)

    return quadrant_a == quadrant_b


def get_quadrant_index(location, center_x, center_y):
    """
    Function to determine the quadrant index for a given location based on the center point.

    Args:
        location (Location): the location of a gate
        center_x (float): the x-coordinate of the center point
        center_y (float): the y-coordinate of the center point

    Returns:
        int: the quadrant index (0, 1, 2, 3) based on the location
    """
    x = location.x
    y = location.y

    # Quadrant 1
    if x <= center_x and y <= center_y:
        return 0

    # Quadrant 2
    elif x > center_x and y <= center_y:
        return 1

    # Quadrant 3
    elif x <= center_x and y > center_y:
        return 2

    # Quadrant 4
    else:
        return 3
