from PIL import Image, ImageDraw
from sympy.ntheory.factor_ import factorint
import numpy as np
import argparse

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

    parser = argparse.ArgumentParser(description='Create a gif of N dots orbiting each other based on the factorization of N.')
    parser.add_argument('N', type=int,
                        help='number of dots in the gif')
    parser.add_argument('-f', '--frames', type=int, default=500,
                        help='number of frames in the resulting gif, which changes the perceived speed of the animation')

    args = parser.parse_args()
    make_gif(n=args.N, num_tics=args.frames)