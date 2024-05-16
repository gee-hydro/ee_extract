import ee


def cal_ETsum(img):
  r = img.expression("b('Ec') + b('Es') + b('Ei')").rename("ET")
  return r.copyProperties(img, img.propertyNames())


bands_ERA5L = {
    'Pa': 'surface_pressure',  # Pa
    'prcp': 'total_precipitation_sum',  # m
    'Tdew': 'dewpoint_temperature_2m',  # K
    'Tmin': 'temperature_2m_min',
    'Tmax': 'temperature_2m_max',
    'Tavg': 'temperature_2m',
    'Tsoil': 'soil_temperature_level_1',
    'Rns': 'surface_net_solar_radiation_sum',  # J m-2
    'Rnl': 'surface_net_thermal_radiation_sum',
    'Rs': 'surface_solar_radiation_downwards_sum',
    'Rln': 'surface_thermal_radiation_downwards_sum',
    'uwind': 'u_component_of_wind_10m',
    'vwind': 'v_component_of_wind_10m',
    'PET': 'potential_evaporation_sum',  # m
    'ET': 'total_evaporation_sum',
    'Ec': 'evaporation_from_vegetation_transpiration_sum',
    'Es': 'evaporation_from_bare_soil_sum',
    'Ei': 'evaporation_from_the_top_of_canopy_sum'
}


def get_daily_ERA5L():
  return ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR")\
      .select(list(bands_ERA5L.values()), list(bands_ERA5L.keys()))


bands_GLDAS21 = {
    "prcp": "Rainf_f_tavg",  # kg/m^2/s
    "Rln": "LWdown_f_tavg",   # W m-2
    "Rnl": "Lwnet_tavg",
    "Rs": "SWdown_f_tavg",
    "Rns": "Swnet_tavg",
    "q": "Qair_f_inst",       # kg kg-1
    "U10": "Wind_f_inst",
    "Pa": "Psurf_f_inst",     # Pa
    "PET": "PotEvap_tavg",    # W m-2
    "ET": "Evap_tavg",        # kg m-2 s-1
    "Ec": "Tveg_tavg",        # W m-2 s-1
    "Es": "ESoil_tavg",       # W m-2 s-1
    "Ei": "ECanop_tavg",      # W m-2 s-1
    "Tsurf": "AvgSurfT_inst",  # K
    "Tair": "Tair_f_inst"
}

def get_GLDAS():
    return ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H")\
        .select(list(bands_GLDAS21.values()), list(bands_GLDAS21.keys()))

# Example usage:
# result = aggregate(imgcol, 'prop', ee.Reducer.mean())
