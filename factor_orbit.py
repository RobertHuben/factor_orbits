from PIL import Image, ImageDraw
import random
from sympy.ntheory.factor_ import factorint
import numpy as np

def make_frame(n, time):
    image = Image.new("RGB", (400, 400), "black")
    draw = ImageDraw.Draw(image)
    center=(200,200)
    point_size=np.array([3,3])
    base_radius=180

    factors=factorint(n)
    positions=np.zeros((n,2))
    max_scale_factor=0
    this_circle_radius=1

    for prime, total_power in factors.items():
        for power in range(1,total_power+1):
            this_circle_radius/=2.5
            frequency=(prime**(power))
            base_offsets=np.arange(prime)/prime
            offsets=np.tile(np.repeat(base_offsets, frequency//prime), n//frequency)
            max_scale_factor+=this_circle_radius
            y_positions=np.sin(2*np.pi*(frequency*time+offsets))
            x_positions=np.cos(2*np.pi*(frequency*time+offsets))
            positions+=this_circle_radius*np.stack((x_positions, y_positions), axis=1)
    
    positions=(base_radius/max_scale_factor)*positions+center
    for point in positions:
        draw.ellipse((tuple(point-point_size), tuple(point+point_size)), fill=(255, 255, 255, 255))

    return image


def make_gif(n, num_tics=200):
    frames = []
    for i in range(num_tics):
        frames.append(make_frame(n, i/num_tics))
    frame_one = frames[0]
    frame_one.save(f"orbit_{n}.gif", format="GIF", append_images=frames[1:],
                   save_all=True, duration=50, loop=0)



if __name__ == "__main__":
    # n_set=[2,4,7,10]
    # n_set=[2,7]
    n_set=[210]
    # n_set=[8]
    # n_set=[135]
    for n in n_set:
        # n=2
        num_tics=500
        make_gif(n, num_tics)