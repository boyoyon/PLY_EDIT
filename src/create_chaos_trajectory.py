import numpy as np
from scipy.integrate import odeint

def odef(trajectory,t,sigma,rho,beta):
    x,y,z = trajectory
    return [sigma*(y-x),x*(rho-z)-y,x*y -beta*z]

def create_trajectory(nr_points=10000):

    # time step (0～25を10,0001分割)
    t = np.linspace(0,25,nr_points)

    initial_location = [1,1,1]
    sigma, rho, beta = 8, 28, 8/3

    trajectory = odeint(odef,initial_location,t, args=(sigma,rho,beta))

    return trajectory

def main():

    trajectory = create_trajectory(10000)
    
    print('trajectory.shape', trajectory.shape)
    np.save('chaos_trajectory.npy', trajectory)
    print('save chaos_trajectory.npy')

if __name__ == "__main__":
    main()
