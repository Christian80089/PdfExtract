import pandas as pd

info_to_extract = [
    "minimo_mensile (è un double ed è mandatory)",
    "periodo_estratto_conto (è una string ed è mandatory, esempio: Novembre 2024)"
    "costo_al_km (è un double ed è mandatory",
    "targa (è una string ed è mandatory)",
    "km_percorsi (è un intero ed è mandatory)",
    "km_inclusi (è un intero ed è mandatory)",
    "km_da_pagare (è un intero ed è mandatory)",
    "km_residui (è un intero ed è mandatory)",
    "premio_di_conguaglio (è un double ed è mandatory)",
    "totale_pagato (è un double ed è mandatory)"
]

mandatory_fields = [
    "minimo_mensile",
    "periodo_estratto_conto",
    "costo_al_km",
    "targa",
    "km_percorsi",
    "km_inclusi",
    "km_da_pagare",
    "km_residui",
    "premio_di_conguaglio",
    "totale_pagato"
]

columns_to_select = [
    "periodo_estratto_conto",
    "date_estratto_conto",
    "targa",
    "minimo_mensile",
    "costo_al_km",
    "km_percorsi",
    "km_inclusi",
    "km_da_pagare",
    "km_residui",
    "premio_di_conguaglio",
    "totale_pagato",
    "note"
]

schema = {
    "periodo_estratto_conto": str,
    "date_estratto_conto": "datetime64[ns]",
    "targa": str,
    "minimo_mensile": float,
    "costo_al_km": float,
    "km_percorsi": int,
    "km_inclusi": int,
    "km_da_pagare": int,
    "km_residui": int,
    "premio_di_conguaglio": float,
    "totale_pagato": float,
    "note": str
}

# Valori predefiniti per i tipi
default_values = {
    str: "",
    "datetime64[ns]": pd.NaT,
    float: 0.0,
    int: 0
}
