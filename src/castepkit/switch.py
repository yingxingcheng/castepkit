from __future__ import annotations

from pathlib import Path

from castep_outputs import parse_cell_param_file

__all__ = ["create_switch_file"]


def _lookup(key, mapping):
    if key in mapping:
        return mapping[key]
    if isinstance(key, tuple) and key[0] in mapping:
        return mapping[key[0]]
    raise KeyError(f"Missing entry for {key}")


def create_switch_file(
    fn_cell: str | Path,
    radius_dict: dict,
    cut_dict: dict,
    *,
    fn_switch: str | Path | None = None,
) -> Path:
    """Create a ``.switch`` file for ``atom_cutting``.

    Parameters
    ----------
    fn_cell : str or Path
        Path to the CASTEP ``.cell`` file.
    radius_dict : dict
        Mapping from atom label to cutting radius in angstrom.
        Keys can be element symbols (e.g. ``"Ga"``) or tuples like
        ``("Ga", 1)`` matching the ``positions_frac`` keys returned by
        :func:`castep_outputs.parse_cell_param_file`.
    cut_dict : dict
        Mapping from atom label to the action ``"keep"`` or ``"cut"``.
    fn_switch : str or Path, optional
        Output file name. Defaults to ``<prefix>.switch`` where ``prefix`` is
        derived from ``fn_cell``.

    Returns
    -------
    Path
        Path to the created switch file.
    """
    fn_cell = Path(fn_cell)
    if fn_switch is None:
        fn_switch = fn_cell.with_suffix(".switch")
    fn_switch = Path(fn_switch)

    with fn_cell.open() as f:
        data = parse_cell_param_file(f)[0]

    atoms = list(data.get("positions_frac", {}).keys())

    lines = ["%BLOCK ATOM_DOMAIN"]
    for atom in atoms:
        element = atom[0] if isinstance(atom, tuple) else atom
        radius = _lookup(atom, radius_dict)
        radius_str = str(radius)
        if isinstance(radius, (int, float)):
            radius_str = f"{radius}d0"
        elif not radius_str.lower().endswith("d0"):
            radius_str += "d0"
        lines.append(f"{element} {radius_str}")
    lines.append("%ENDBLOCK ATOM_DOMAIN")
    lines.append("")
    lines.append("%BLOCK CUT_ATOM")
    for atom in atoms:
        element = atom[0] if isinstance(atom, tuple) else atom
        action = _lookup(atom, cut_dict)
        if isinstance(action, bool) or isinstance(action, int):
            action = "keep" if bool(action) else "cut"
        lines.append(f"{element}      {action} 2")
    lines.append("%ENDBLOCK CUT_ATOM")

    fn_switch.write_text("\n".join(lines) + "\n")
    return fn_switch
