from PIL import Image, ImageDraw
from sympy.ntheory.factor_ import factorint
import numpy as np
import argparse

def make_frame(n:int, time:float) -> Image:
    """ makes one frame of the gif of n orbiting points.

    Args:
        n: The number of points to animate.
        time: How far into the animation this frame will be. Should be between 0 and 1, since the animation loops with period 1.

    Returns:
        image: The PIL image of the points.
    """
    image_size=400
    center=(image_size/2,image_size/2)
    point_size=np.array([3,3])
    final_radius=180 # final image will be scaled to live in a circle with this radius

    image = Image.new("RGB", (image_size, image_size), "black")
    draw = ImageDraw.Draw(image)
    factors=factorint(n)

    '''
    point locations are the sum of epicycles
    there is one epicycle per factor
    each epicycle has a different radius and rotational frequency
    each point within the epicycle has one of p=prime different phase shifts
    '''
    point_locations=np.zeros((n,2)) #positions of the points to draw, built up over the method
    current_scale_factor=1 # radius of the current epicycle
    epicycle_scale_ratio=2.5 # determines the amount current_scale_factor shrinks by for each epicycle
    total_scale_factor=0 # running sum of the scaling to do in the final step
    for prime, total_power in factors.items():
        for power in range(1,total_power+1):
            current_scale_factor/=epicycle_scale_ratio
            total_scale_factor+=current_scale_factor
            orbit_frequency=prime**(power)
            base_phase_shifts=np.arange(prime)/prime # these will be repeated and tiled to make the phase shifts for all points
            phase_shifts=np.tile(np.repeat(base_phase_shifts, orbit_frequency//prime), n//orbit_frequency)
            y_positions=np.sin(2*np.pi*(orbit_frequency*time+phase_shifts))
            x_positions=np.cos(2*np.pi*(orbit_frequency*time+phase_shifts))
            point_locations+=current_scale_factor*np.stack((x_positions, y_positions), axis=1)
    
    point_locations=(final_radius/total_scale_factor)*point_locations+center # uniformly scale and shift
    for point in point_locations:
        draw.ellipse((tuple(point-point_size), tuple(point+point_size)), fill=(255, 255, 255, 255))

    return image


def make_gif(n:int, num_frames:int=200):
    """ makes a gif of the n points orbiting the center.

    Args:
        n: The number of points to animate.
        num_frames: The number of frames to spread the animation over.
    """
    frames = [make_frame(n, i/num_frames) for i in range(num_frames)]
    first_frame = frames[0]
    first_frame.save(f"orbit_{n}.gif", format="GIF", append_images=frames[1:],
                   save_all=True, duration=50, loop=0)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create a gif of N dots orbiting each other based on the factorization of N.')
    parser.add_argument('N', type=int,
                        help='number of dots in the gif')
    parser.add_argument('-f', '--frames', type=int, default=500,
                        help='number of frames in the resulting gif, which changes the perceived speed of the animation')

    args = parser.parse_args()
    make_gif(n=args.N, num_frames=args.frames)