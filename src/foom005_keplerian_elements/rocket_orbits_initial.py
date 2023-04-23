'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Fundamentals of Orbital Mechanics 5
Introduction to Keplerian Orbital Elements

Create orbit SPICE BSP kernel for 4 orbits
with different orbital planes
'''

# 3rd party libraries
import spiceypy as spice
import os
# AWP library
import numerical_tools    as nt
import orbit_calculations as oc
import plotting_tools     as pt
import spice_data         as sd
import numpy as np
if __name__ == '__main__':
	spice.furnsh( sd.leapseconds_kernel )
	spice.furnsh( sd.pck00010 )

	coes_list   = []
	states_list = []
	tspan       = 24 * 3600.0 * 7
	dt          = 10.0

	coes_list.append( [ 25000.0, 0.4, 30,  0, 0,   30  ] )
	# coes_list.append( [ 15000.0, 0.4, 30,  0, 40,  60  ] )
	# coes_list.append( [ 15000.0, 0.4, 75,  0, 270, 60  ] )
	# coes_list.append( [ 15000.0, 0.4, 100, 0, 270, 100 ] )
	radial0, lat0, lon0 = 7000, 28.396837 / 180 * np.pi, -80.605659 / 180 * np.pi
	# radial0, lat0, lon0 = 403626.33, -18.2656 / 180 * np.pi, -98.3495 / 180 * np.pi
# Radius     (km):      403626.33912495
# Longitude (deg):         -98.34959789
# Latitude  (deg):         -18.26566077
	r_ecef = spice.latrec(radial0, lon0, lat0)
	print('r_ecef', r_ecef)
	ets = spice.str2et( '2021-12-26')
	Q = spice.pxform('IAU_EARTH', 'J2000', ets)
	r_j2000 = np.matmul(Q, r_ecef)
	print('r_ecef', r_ecef)
	print('rj2000', r_j2000)
	# print('x0, y0, z0', x0, y0, z0)
	vx0 = -10
	vy0 = 60
	vz0 = 0
	x0, y0, z0 = r_j2000

	initial = np.array([[x0, y0, z0]])
	print('initial shape', initial.shape)
	# radial, longitude, latitude
	# radial2, lon2, lat2 = spice.reclat([x0, y0, z0])
	# print(' spice.reclat', radial2, lon2 * 180/np.pi, lat2 * 180/np.pi)
	print('cart2lat', nt.cart2lat(initial, 'J2000', 'IAU_EARTH', [ets] ))  # should match launch site lat/lng again
	m0 = 4.21e6
	for coes in coes_list:
		# print('Determine the state', state0)
		state0  = [x0, y0, z0, vx0, vy0, vz0]
		# state0      = oc.coes2state( coes )

		print('state0', state0)
		ets, states = nt.propagate_ode(
			oc.two_body_ode, state0, tspan, dt)

		states_list.append( states[:, :6] )

	pt.plot_orbits( states_list, {
		'labels'  : [ '0', '45', '75', '100' ],
		'colors'  : [ 'crimson', 'lime', 'c', 'm' ],
		'traj_lws': 2,
		'show'    : True
	} )

	ets    += spice.str2et( '2021-12-26' )
	latlons = []
	for states in states_list:
		latlons.append( nt.cart2lat(
			states[ :3000, :3 ], 'J2000', 'IAU_EARTH', ets ) )
	print(states.shape)

	pt.plot_groundtracks( latlons, {
		'labels'  : [ '0', '45', '75', '100' ],
		'colors'  : [ 'crimson', 'lime', 'c', 'm' ],
		'show'    : True
	} )

	'''
	This part is outside the scope of this lesson, but for those
	who are curious this is how to write the trajectory to a
	SPICE .bsp kernel to then use in Cosmographia
	In general, it is bad practice to have imports in this
	part of the code, so don't try this at home!
	'''
	if True:
		import spice_tools  as st
		spice.furnsh( sd.leapseconds_kernel )
		file = 'many-orbits.bsp'
		if os.path.exists(file):
			os.remove(file)
		else:
			print("The file does not exist")

		print('states list [0] length', len(states_list[0]))
		print('ets shape', ets.shape)
		st.write_bsp( ets, states_list[ 0 ], {
			'bsp_fn': 'many-orbits.bsp',
			'spice_id': -999,
		} )

		# for n in [ 1, 2, 3 ]:
		# 	st.write_bsp( ets, states_list[ n ], {
		# 		'bsp_fn'  : 'many-orbits1.bsp',
		# 		'spice_id': -999 + n,
		# 		'new'     : False
		# 	} )
