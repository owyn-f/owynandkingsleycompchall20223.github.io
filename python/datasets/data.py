import pandas as pd

df = pd.read_csv('exo planet data .csv', skiprows=10)
#orbeccen - eccentricity
#pl_orbper - orbital period(days)
#pl_orbsmax - semi major axis(au)
#glat, glon, elat, elon - eclepitc/galctic latitude/longitude
#hostname- system name
#pl_name - planet name

values_dict = {
    'name': 1,
    'system_name': 2,
    'a': 4,
    'ecc': 5,
    'beta': 6,
    'period': 3
}

def get_system(system):
    return list(df.index[df['hostname'] == system])
    # list of planet indexes

def get_values(values, pl_index):
    idx = []
    for value in values:
        idx.append(values_dict[value])
    pl_values = []
    for i in idx:
        pl_values.append(df.iloc[pl_index, i])
    return pl_values
