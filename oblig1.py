#Oppgave A)
#ENDRER DATETIME OGSÅ SETTER DEN TIL DEN 15 HVER MÅNED.

df['måned'] = pd.to_datetime(df['måned'], format='%YM%m')
df['måned'] = df['måned'] + pd.to_timedelta(14, unit='d')
df

#Fjerner xa0
df["ulykkestype"] = df["ulykkestype"].str.replace('\xa0', "")

#Oppgave B)
df["baremåned"] = df["måned"].dt.year
df

drept_data = df[df["skadegrad"] == "Drept"].groupby("måned")["08329: Drepte eller skadde i trafikkulykker,"].sum()
drept_data

drept_data.plot(x="år", y="08329: Drepte eller skadde i trafikkulykker,", kind="line", figsize=(10, 5), title="Antall drept per måned")

#Oppgave c)
ikke_drept_data = df[df["skadegrad"] != "Drept"]
månedlig_ikke_drept = ikke_drept_data.groupby(df["måned"].dt.month)["08329: Drepte eller skadde i trafikkulykker,"].sum()

månedlig_ikke_drept.plot(x="måned", y="Antall drept", kind="line", figsize=(10, 5), title="Antall drept per måned")

#Oppgave d)

df["baremåned"] = df["måned"].dt.year

drept_data = df[df["skadegrad"] != "Skadde i alt"]

pivot_table = drept_data.pivot_table(index="måned", columns="skadegrad", values="08329: Drepte eller skadde i trafikkulykker,", aggfunc="sum")

pivot_table.plot(kind="line", figsize=(10, 5))
plt.title("Antall drept per måned (skadegrad)")
plt.xlabel("år")
plt.ylabel("Antall drept eller skadde")
plt.legend(title="Skadegrad", bbox_to_anchor=(1.05, 1), loc='upper left')


#Oppgave e)

df["baremåned"] = df["måned"].dt.year

drept_data = df[(df["ulykkestype"] == "C. Møting ved forbikjøring") | (df["ulykkestype"] == "D. Andre møteulykker")]

pivot_table = drept_data.pivot_table(index="måned", columns="ulykkestype", values="08329: Drepte eller skadde i trafikkulykker,", aggfunc="sum")

pivot_table.plot(kind="line", figsize=(15, 10))
plt.title("")
plt.xlabel("år")
plt.ylabel("")
plt.legend(title="Skadegrad", bbox_to_anchor=(1.05, 1), loc='upper left')

#oppgave F)

file_path_to_csv = "trafikkindeks_fra_1995.csv"
df_trafikkdata = pd.read_csv(file_path_to_csv)
df_trafikkdata
df_trafikkdata = df_trafikkdata.rename(columns={'måned': 'baremåned'}) #for å matche df og den nye csv’en 
Sammensatt_df = pd.merge(df, df_trafikkdata, on="baremåned") #kombiner df’ene
drept_data = Sammensatt_df.groupby("baremåned")["08329: Drepte eller skadde i trafikkulykker,"].sum()
drept_data.plot(kind="line", figsize=(10, 5), title="Antall drept per år")


