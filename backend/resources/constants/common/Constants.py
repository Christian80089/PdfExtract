import pandas as pd

df_default_values = {
    str: "",
    "datetime64[ns]": pd.NaT,
    float: 0.0,
    int: 0
}

airtable_personal_token = "patsk5OLlCCaeLvot.2ee28ebda52370ba08c23582b78af71d7ad57caea704a4176669f6b95b39dbeb"
airtable_pdfextract_base_id = "appGAiaKoPaJym0CB"

aiven_postgresql_db_host = "pg-34992b48-cdelprete972-6ad9.b.aivencloud.com"
aiven_postgresql_db_port = "24092"
aiven_postgresql_db_username = "avnadmin"
aiven_postgresql_db_password = "AVNS__fw4ruPbauocp_OC1--"
aiven_postgresql_db_default_name = "defaultdb"
aiven_postgresql_db_name = "pdfextract"
