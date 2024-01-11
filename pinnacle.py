def add_bin_depth(data, depth_variable = 'NAV_DEPTH'):
    """
    Add a varaible 'bin_depth' with depth of each range cell, based on the AUV depth.
    
    Parameters:
        data : xarray dataset with pinnacle data 
        depth_variable: Name of variable to use for depth
    """
    return data.assign(bin_depth = (data[depth_variable] - data.range))


def find_surface_level(data, mode='max++', zmax=100, rmin=100,
                       depth_variable = 'NAV_DEPTH', backscatter_variable = 'SerEAAcnt'):
    """
    Detects surface based on back scatter level from pinnacle data.
    
    Parameters:
        data : xarray dataset with pinnacle data 
        mode : 'max'  : Detects the range cell with maximum amplitude
               'max+' : As 'max', but ignores range cells above zmax meters above surface (which 
                        is defined based on AUV depth).
               'max++': As 'max+', but ignores range cells closer than rmin meters to the ADCP
        
    Return:
        A new xarray dataset with added variables:
            distance_to_surface : The distance to the detected surface (from the ADCP)
            surface_level       : z-coordinate of the detected surface, based on AUV depth.
            (bin_depth          : Depth of each range cell, based on the AUV depth )
    """  
    if not 'bin_depth' in data.keys():
        data = add_bin_depth(data, depth_variable = depth_variable)
    
    if mode == 'max':
        # Just a basic max 
        amp = data[backscatter_variable].dropna('time')

    if mode == 'max+':
        # Max must not be above surface
        amp = data.where(-data.bin_depth < zmax,0)[backscatter_variable].dropna('time')
        
    if mode == 'max++':
        # Max must not be above surface + not in first range bin
        amp = data.where(-data.bin_depth < zmax,0)[backscatter_variable].dropna('time')
        amp = amp.where(amp.range>rmin,0)
    
    distance_to_surface = data.range[amp.argmax(dim='range',skipna=True)]
    surface_level = -data[depth_variable] + data.range[amp.argmax(dim='range',skipna=True)]
        
    return data.assign(surface_level = surface_level.round(), 
                       distance_to_surface = distance_to_surface.round())