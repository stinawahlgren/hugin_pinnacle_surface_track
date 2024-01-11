import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator, HourLocator

def pcolormesh_offset(x,y,z,y_offset, x_pixel_scale = None, vmin = None, vmax = None, **kwargs):
    """
    Example:
        Ny = 300
        Nx = 400
        x  = np.arange(Nx)
        y  = np.arange(Ny)
        z  = np.random.rand(Ny, Nx)
        y_offset = np.linspace(0,50,Nx)
        pcolormesh_offset(x, y, z, y_offset)
    """    
    (Ny, Nx) = z.shape
    
    if Ny != len(y):
        raise ValueError('y must have same length as first dimension of z')
        
    if Nx != len(x):
        raise ValueError('x must have same length as second dimension of z')
        
    if len(y_offset) != Nx:
        raise ValueError('y_offset must have same length as second dimension of z') 
        
    if vmin is None:
        vmin = np.nanmin(z)
    
    if vmax is None:
        vmax = np.nanmax(z)
        
    # Deal with nan in offset
    nan_offset = np.isnan(y_offset)   
    y_offset[nan_offset] = 0
    z[:,nan_offset] = np.nan
        
    x_edges = _get_edges(x)
    y_edges = _get_edges(y)
                             
    for i in range(Nx):
        if x_pixel_scale is None:
            x_edge = x_edges[i:(i+2)]
        else:
            x_center = (x_edges[i]+x_edges[i+1])/2
            x_edge   = np.array([-0.5,0.5])* x_pixel_scale * x_step + x_center
            
        plt.pcolormesh(x_edge, y_offset[i]+y_edges, z[:,i:i+1], vmin=vmin, vmax=vmax, **kwargs)
      
    plt.xlim(x_edges[0], x_edges[-1])
    return

def nice_time_axis(ax=None):
    if ax is None:
        ax = plt.gca()
    ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_minor_locator(HourLocator([0,3,6,9,12,15,18,21]))
    ax.xaxis.set_major_formatter(DateFormatter("%Y %b %d"))
    ax.xaxis.set_minor_formatter(DateFormatter("%H:%M"))
    ax.get_xaxis().set_tick_params(which='major', pad=10)

def _get_edges(centers):
    centers = np.array(centers)
    mid = centers[:-1] + (centers[1:]-centers[:-1])/2
    first = centers[0] - (centers[1]-centers[0])/2
    last  = centers[-1] + (centers[-1]-centers[-2])/2
    return np.concatenate([[first], mid, [last]])