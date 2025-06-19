import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from math import sin, asin, radians, degrees, tan, cos

# Load custom font for Chinese text
font_path = "font.otf"  # Ensure this path is correct
custom_font = FontProperties(fname=font_path)

# Set Streamlit page
st.title("光線折射模擬")
st.write("調整入射角和介質折射率，觀察光線路徑變化")

# Sidebar inputs
st.sidebar.header("參數設置")
incident_angle = st.sidebar.slider("入射角 (度)", 0, 90, 45)
n1 = st.sidebar.slider("介質1折射率 (n1)", 1.0, 3.0, 1.0, step=0.1)
n2 = st.sidebar.slider("介質2折射率 (n2)", 1.0, 3.0, 1.5, step=0.1)

# Calculate refraction angle (Snell's Law: n1 * sin(θ1) = n2 * sin(θ2))
theta1 = radians(incident_angle)
sin_theta2 = n1 * sin(theta1) / n2

# Check for total internal reflection
if sin_theta2 > 1:
    st.warning("發生全反射！折射角不存在。")
    theta2 = None
else:
    theta2 = asin(sin_theta2)
    st.write(f"折射角: {degrees(theta2):.2f} 度")

# Create plot
fig, ax = plt.subplots(figsize=(8, 6))

# Set axes, ensuring origin (0, 0) is at the center
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.grid(True)

# Draw interface (y=0)
ax.axhline(0, color='black', linestyle='--')

# Incident ray: From top-left (x<0, y>0) to origin (0, 0)
x_start = -1.0
y_start = tan(radians(90 - incident_angle)) * abs(x_start)  # Angle relative to x-axis
x_incident = np.array([x_start, 0.0])
y_incident = np.array([y_start, 0.0])
ax.plot(x_incident, y_incident, 'b-', label='入射光線')

# Draw normal (at origin, along y-axis)
ax.plot([0, 0], [-1.5, 1.5], 'k:', label='法線')

# Refracted ray: From origin (0, 0) to bottom-right (x>0, y<0)
if theta2 is not None:
    x_end = 1.0
    y_end = -tan(radians(90 - degrees(theta2))) * x_end  # Angle relative to x-axis
    x_refracted = np.array([0.0, x_end])
    y_refracted = np.array([0.0, y_end])
    ax.plot(x_refracted, y_refracted, 'r-', label='折射光線')
else:
    # Total internal reflection: Reflection angle equals incident angle
    x_end = -1.0
    y_end = tan(radians(90 - incident_angle)) * abs(x_end)
    x_reflected = np.array([0.0, x_end])
    y_reflected = np.array([0.0, y_end])
    ax.plot(x_reflected, y_reflected, 'g-', label='反射光線')

# Add labels and legend with custom font
ax.text(-1.4, 1, f'介質1 (n1 = {n1})', fontsize=12, fontproperties=custom_font)
ax.text(-1.4, -1, f'介質2 (n2 = {n2})', fontsize=12, fontproperties=custom_font)
ax.legend(prop=custom_font)
ax.set_xlabel('X', fontproperties=custom_font)
ax.set_ylabel('Y', fontproperties=custom_font)
ax.set_title('光線折射模擬', fontproperties=custom_font)

# Display plot
st.pyplot(fig)

# Description
st.write("""
### 模擬說明
- **入射角**: 光線從介質1（左上，x<0, y>0）射向原點 (0, 0) 的角度，範圍0°到90°，相對於法線（y 軸）。
- **折射率**: 介質1 (n1) 和介質2 (n2) 的折射率，範圍1.0到3.0。
- **斯涅爾定律**: n1 * sin(θ1) = n2 * sin(θ2)。
- 光線從左上射向原點，折射後從右下 (x>0, y<0) 射出。若發生全反射，光線回到介質1 (y>0)。
""")