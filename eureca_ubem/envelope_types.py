"""
This module includes a container class for envelope types
"""

__author__ = "Enrico Prataviera"
__credits__ = ["Enrico Prataviera"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Enrico Prataviera"

'''IMPORTING MODULES'''

import pandas as pd
from eureca_building.construction_dataset import ConstructionDataset
from eureca_building.construction import Construction
from eureca_building.window import SimpleWindow

# %% ---------------------------------------------------------------------------------------------------
# %% Useful functions

def load_envelopes(path):
    '''
    load_envelopes loads all materials, windows, stratigraphies and envelopes
    archetypes in a database that is then utilized by the main program

    Parameters
    ----------
    path : string
        Path containing the string of the Buildings_Envelopes.xlsx
    Returns
    -------
    envelopes_dict: dictionary with archetype_key/Envelope(object) data

    '''

    if not isinstance(path, str):
        raise TypeError(f'load_envelopes function, input path is not a string. path type: {type(path)}')

    cs_dataset = ConstructionDataset.read_excel(path)
    # Materials and constructions are loaded through the eureca-building library

    try:
        envelopes = pd.read_excel(path, sheet_name="Envelopes", header=[0], index_col=[0])
    except FileNotFoundError:
        raise FileNotFoundError(f'ERROR Failed to open the archetype xlsx file {path}... Insert a proper path')

    envelopes_dict = dict()
    for i in envelopes.index:
        envelope = EnvelopeType(
            name = envelopes.loc[i]["name"],
            roof = cs_dataset.constructions_dict[envelopes.loc[i]["Roof"]],
            ground_floor = cs_dataset.constructions_dict[envelopes.loc[i]["GroundFloor"]],
            interior_ceiling = cs_dataset.constructions_dict[envelopes.loc[i]["IntCeiling"]],
            external_wall = cs_dataset.constructions_dict[envelopes.loc[i]["ExtWall"]],
            interior_wall = cs_dataset.constructions_dict[envelopes.loc[i]["IntWall"]],
            window = cs_dataset.windows_dict[envelopes.loc[i]["Window"]],
        )

        envelopes_dict[envelope.name] = envelope

    return envelopes_dict


# %%---------------------------------------------------------------------------------------------------
# %% EnvelopeType class

class EnvelopeType(object):
    '''
    Definition of the EnvelopeType class
    Each object of EnvelopeType contains several informations about stratigraphies

    Methods:
        init
    '''

    def __init__(self,
                 name: str,
                 roof: Construction,
                 ground_floor: Construction,
                 interior_ceiling: Construction,
                 external_wall: Construction,
                 interior_wall: Construction,
                 window: SimpleWindow,
                 ):
        """
        Create an envelope type

        Parameters
        ----------
        name: str,
            Name
        roof: Construction
            roof construction obj
        ground_floor: Construction
            ground_floor construction obj
        interior_ceiling: Construction
            interior_ceiling construction obj
        external_wall: Construction
            external_wall construction obj
        interior_wall: Construction
            interior_wall construction obj
        window: Construction
            window construction obj
        """

        self.name = name
        self.roof = roof
        self.ground_floor = ground_floor
        self.external_wall = external_wall
        self.interior_wall = interior_wall
        self.interior_ceiling = interior_ceiling
        self.interior_floor = Construction(
            name = self.interior_ceiling.name + "_flipped",
            materials_list = list(reversed(self.interior_ceiling.materials_list)),
            construction_type = "IntFloor",
        )
        self.window = window
