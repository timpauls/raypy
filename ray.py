#!/usr/bin/python

from geometry import Plane, Sphere, Triangle, Cube
from scene import Screen, Scene
from tracer import SimpleRayTracer, SimpleShadowRayTracer, ShadingShadowRayTracer, RecursiveRayTracer, PathTracer
from material import Material, Color
from window import Window

if __name__ == "__main__":
	p1 = Plane([0, 5, 0], [0, -1, 0], Material(Color(255, 0, 0), 1, 0, 0.1))
	p2 = Plane([0, -5, 0], [0, 1, 0], Material(Color(0, 255, 0), 1, 0, 0.1))
	p3 = Plane([5, 0, 0], [-1, 0, 0], Material(Color(0, 0, 255), 1, 0, 0.1))
	p4 = Plane([-5, 0, 0], [1, 0, 0], Material(Color(255, 255, 0), 1, 0, 0.1))
	p5 = Plane([0, 0, 5], [0, 0, -1], Material(Color(255, 0, 255), 1, 0, 0.1))
	p6 = Plane([0, 0, -5], [0, 0, 1], Material(Color(0, 255, 255), 1, 0, 0.1))

	s1 = Sphere([0, 3, 2], 2, Material(Color(100, 100, 100), 1, 0, 0.1, refractive=False, n=1.52))
	s2 = Sphere([4, 2, 1], 0.5, Material(Color(100, 100, 100), 1, 0, 0.1, refractive=False, n=1.52))
	s3 = Sphere([-3, 2, 1], 1, Material(Color(100, 100, 100), 1, 0, 0.1, refractive=False, n=1.52))
	s4 = Sphere([2, -2, 1], 0.8, Material(Color(100, 100, 100), 1, 0, 0.1, refractive=False, n=1.52))

	center = [0, 4, 0]
	length = 2
	cube_color = Color(125, 125, 125)

	#c1 = Cube(center, length, Material(cube_color, 1, 1, 0.1))

	l1 = Sphere([-3, -2.5, 3], 1, Material(Color(255, 255, 255), 1, 1, 1))
	l2 = Sphere([3, -2.5, -3], 1, Material(Color(255, 255, 255), 1, 1, 1))

	eye = [0, 0, -4.9]

	import argparse
	parser = argparse.ArgumentParser(description="Ray Tracing in Python.")
	parser.add_argument("-r", "--render", help="activate non-interactive rendering into a file.", nargs=2,
						metavar=("FILENAME", "ALGORITHM"))
	parser.add_argument("--width", type=int, help="width of the image.", default=200)
	parser.add_argument("--height", type=int, help="height of the image.", default=200)

	args = parser.parse_args()

	WIDTH = args.width
	HEIGHT = args.height
	bla = 10.0 / WIDTH
	screen = Screen([0, 0, -1], [0, 0, -1], WIDTH, HEIGHT, bla)
	scene = Scene(eye=eye, screen=screen, geometry=[p1, p2, p3, p4, p5, p6, s1, s2, s3, s4], lights=[l1,l2])

	if not args.render is None:
		print "rendering mode into: %s with %s" % (args.render[0], args.render[1])
		from filerenderer import FileRenderer

		value = args.render[1]

		if value == "Simple":
			tracer = SimpleRayTracer()
		elif value == "Shadow":
			tracer = SimpleShadowRayTracer()
		elif value == "ShadingShadow":
			tracer = ShadingShadowRayTracer(scene.eye)
		elif value == "Recursive":
			tracer = RecursiveRayTracer(scene.eye)
		elif value == "PathTracing":
			tracer = PathTracer(scene.eye)
		else:
			print "Unknown Ray-Tracer Algorithm. Exiting ..."
			exit(1)

		renderer = FileRenderer(WIDTH, HEIGHT, tracer, scene)
		renderer.render(args.render[0])
	else:
		window = Window(WIDTH, HEIGHT, scene, tracer=SimpleRayTracer())
