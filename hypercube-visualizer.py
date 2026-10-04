# -*- coding: utf-8 -*-
# Author: Roopesh Singh
# License: MIT (https://opensource.org/licenses/MIT)

import numpy as np
import matplotlib.pyplot as plt

def generate_hypercube(dimensions):
    """
    Recursively builds an n-dimensional hypercube vertex set and edge list 
    using the sweep-and-mirror geometric method.
    """
    if dimensions < 1:
        raise ValueError("Dimensions must be at least 1.")
        
    # Base case: 1D line segment
    vertices = np.array([[0.0], [1.0]])
    edges = [(0, 1)]
    
    # Recursively scale up to the target dimension
    for dim in range(1, dimensions):
        num_v = len(vertices)
        
        # 1. Sweep and Mirror: duplicate vertices along a new orthogonal axis
        new_vertices = np.zeros((num_v * 2, dim + 1))
        new_vertices[:num_v, :dim] = vertices
        new_vertices[:num_v, dim] = 0.0
        
        new_vertices[num_v:, :dim] = vertices
        new_vertices[num_v:, dim] = 1.0
        
        # 2. Connection: bridge old edges and connect corresponding cross-axis vertices
        new_edges = list(edges)
        for edge in edges:
            new_edges.append((edge[0] + num_v, edge[1] + num_v))
        for i in range(num_v):
            new_edges.append((i, i + num_v))
            
        vertices = new_vertices
        edges = new_edges
        
    # Center around the origin (-0.5 to 0.5) for symmetric rotation
    return vertices - 0.5, edges

def rotate_n_dim(vertices, angle, dim):
    """
    Applies multi-plane orthogonal rotations in n-dimensional space.
    """
    if dim < 4:
        return vertices  # 1D, 2D, and 3D handle rotation during projection/viewing
        
    v_rot = vertices.copy()
    
    # Rotation in the primary higher-dimensional plane (Axis 0 vs Axis dim-1)
    c1, s1 = np.cos(angle), np.sin(angle)
    R1 = np.eye(dim)
    R1[0, 0] = c1
    R1[0, dim - 1] = -s1
    R1[dim - 1, 0] = s1
    R1[dim - 1, dim - 1] = c1
    v_rot = np.dot(v_rot, R1.T)
    
    # Secondary rotation plane for 5D and 6D
    if dim >= 5:
        c2, s2 = np.cos(angle * 0.7), np.sin(angle * 0.7)
        R2 = np.eye(dim)
        R2[1, 1] = c2
        R2[1, dim - 2] = -s2
        R2[dim - 2, 1] = s2
        R2[dim - 2, dim - 2] = c2
        v_rot = np.dot(v_rot, R2.T)
        
    return v_rot

def project_to_3d(vertices, dim, distance=2.2):
    """
    Iteratively projects n-dimensional coordinates down to 3D viewing space 
    and applies scale compensation.
    """
    current = vertices.copy()
    
    # Handle lower dimensions by embedding them into 3D space with larger scale
    if dim == 1:
        res = np.zeros((len(current), 3))
        res[:, 0] = current[:, 0] * 2.2
        return res
    elif dim == 2:
        res = np.zeros((len(current), 3))
        res[:, :2] = current[:, :2] * 2.2
        return res
    elif dim == 3:
        return current * 2.2  # Larger scale for 3D cube
        
    # Iterative perspective projection from dim down to 3
    for d in range(dim, 3, -1):
        projected = []
        for v in current:
            w_coord = v[-1]
            w_factor = 1 / (distance - w_coord)
            p = v[:-1] * w_factor
            projected.append(p)
        current = np.array(projected)
        
    # Scale compensation factors restricted to 4D through 6D
    scale_factors = {
        4: 2.4,
        5: 5.6,
        6: 10.8
    }
    multiplier = scale_factors.get(dim, 2.5)
    
    return current * multiplier

# --- User Input & Execution ---
print("==================================================")
print("  N-DIMENSIONAL HYPERCUBE VISUALIZER (1D - 6D)")
print("==================================================")
try:
    target_dim = int(input("Enter the dimension you want to visualize (1 to 6): "))
    if not (1 <= target_dim <= 6):
        print("Error: Please enter a number between 1 and 6. Defaulting to 4D.")
        target_dim = 4
except ValueError:
    print("Invalid input. Defaulting to 4D Tesseract.")
    target_dim = 4

print(f"\nConstructing and rendering the {target_dim}-dimensional hypercube...")
vertices_nd, edges = generate_hypercube(target_dim)

# Set up matplotlib 3D window
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

angle = 0.0
try:
    while plt.fignum_exists(fig.number):
        ax.cla()
        
        # Apply dimensional rotations and projected scaling down to 3D
        rot_v = rotate_n_dim(vertices_nd, angle, target_dim)
        proj_v = project_to_3d(rot_v, target_dim)
        
        # Render edges
        for edge in edges:
            p1 = proj_v[edge[0]]
            p2 = proj_v[edge[1]]
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='cyan', alpha=0.7, linewidth=1.5)
            
        # Render vertices
        ax.scatter(proj_v[:, 0], proj_v[:, 1], proj_v[:, 2], color='white', s=45)
        
        limit = 1.6
        ax.set_xlim([-limit, limit])
        ax.set_ylim([-limit, limit])
        ax.set_zlim([-limit, limit])
        ax.set_title(f"{target_dim}D Hypercube Projected to 3D", fontsize=12, color='white')
        ax.axis('off')
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        
        plt.draw()
        plt.pause(0.02)
        angle += 0.02
except Exception:
    pass