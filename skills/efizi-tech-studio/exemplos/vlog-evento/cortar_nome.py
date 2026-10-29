import os
def nome(c):
    f, a, b, o = c
    z = f"_z{o['zoom']}" if o.get("zoom") else ""
    z += f"_t{o['tela'][0]}-{o['tela'][1]}" if o.get("tela") else ""
    return f"{os.path.splitext(f)[0]}_{a:.2f}_{b:.2f}{z}.mov"
