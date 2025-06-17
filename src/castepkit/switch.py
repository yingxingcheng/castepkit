from castep_outputs import parse_cell_param_file


def create_switch_file(fn_cell, radius_dict, cut_dict):
    """
    Create a PREFIX.switch file for `cutting_atom` script inluding, e.g.,

    ```
    %BLOCK ATOM_DOMAIN
     Ga 0.79d0
     As 0.79d0
    %ENDBLOCK ATOM_DOMAIN

    %BLOCK CUT_ATOM
    Ga      keep 2
    As      cut 2
    %ENDBLOCK CUT_ATOM
    ```

    where the atom_domain block include the cutting radius for each atom.
    The cut_atom block specify which one is kept and cutted.

    The atom info should be readed from .cell file by using `castep_outputs` package.
    The order and number of atoms should be the same as .cell file.

    The number aster keep or cut is the type of cutting. The default is 2. It could be other numbers, but we
    don't know what is the meaning of them.

    d0 is mandatory and it refers to the unit.
    The unit for this radius is angstrom.

    The radius_dict and cut_dict should including all info.
    For a strucutre with multiple atoms with the same type, we can use ('Ga', 1) index liek in
    in the data from castep_outputs package.

    """

    data = parse_cell_param_file(fn_cell)[0]
    print(data)

    # TODO
