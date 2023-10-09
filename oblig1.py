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

#Oppgave 2 a)

library(lubridate)
parquet_file <- "C:/onemin2015/solar.parquet"
df <- arrow::read_parquet(parquet_file)
df$TIMESTAMP <- lubridate::with_tz(df$TIMESTAMP, tzone = "America/New_York")
library(ggplot2)
df$TIMESTAMP <- as.POSIXct(df$TIMESTAMP)
start_date <- as.POSIXct("2015-06-01") end_date <- as.POSIXct("2015-08-31")
df_filtered <- df[df$TIMESTAMP >= start_date & df$TIMESTAMP <= end_date, ]
ggplot(df_filtered, aes(x = TIMESTAMP, y = Pyra1_Wm2_Avg)) + geom_point() + labs(x = "Timestamp", y = "Pyra1_Wm2_Avg") + ggtitle("Plot of Pyra1_Wm2_Avg Over Time (June 2015 - August 2015)")

Oppgave b)

> df$TIMESTAMP <- as.POSIXct(df$TIMESTAMP)
> start_date <- as.POSIXct("2015-07-01")
> end_date <- as.POSIXct("2015-07-7")
> df_filtered <- df[df$TIMESTAMP >= start_date & df$TIMESTAMP <= end_date, ]
> ggplot(df_filtered, aes(x = TIMESTAMP)) + geom_line(aes(y = Pyra1_Wm2_Avg), color = "blue", size = 1) + geom_line(aes(y = InvPDC_kW_Avg), color = "red", size = 1) + labs(x = "Timestamp", y = "Values") + ggtitle("(June 2015)")


#Oppgave c)

missing_values <- sum(is.na(df$Pyra1_Wm2_Avg) | is.na(df$InvPDC_kW_Avg))
df_cleaned <- df[complete.cases(df$Pyra1_Wm2_Avg, df$InvPDC_kW_Avg), ]
correlation <- cor(df_cleaned$Pyra1_Wm2_Avg, df_cleaned$InvPDC_kW_Avg)
cat("Pearson Correlation between Pyra1_Wm2_Avg and InvPDC_kW_Avg:", correlation, "\n")
#Ettersom den lander på rundt 0.03 vil det si at de er lite avhengige av hverandre og det er svak korrelasjon, det er noe korrelasjon, men den er ikke sterk.
# (dette er tatt fra hele året ikke en uke, om vi tar en uke ser vi høyere korrelasjon, tror dette er grunnet de negative verdiene i datasattet, derfor 1 år har mindre korrelasjon)

#oppgave D)

start_date <- as.POSIXct("2015-07-01")
 end_date <- as.POSIXct("2015-07-07")
df_filtered <- df[df$TIMESTAMP >= start_date & df$TIMESTAMP <= end_date, ]

ggplot(df_filtered, aes(x = InvPDC_kW_Avg, y = Pyra1_Wm2_Avg)) + geom_point() + labs(x = "InvPDC_kW_Avg", y = "Pyra1_Wm2_Avg") + ggtitle("July 1, 2015 - July 7, 2015)")
#Ser igjen at plotten blir bedre om vi tar uke istedefor år, tror dette også er grunnet de neagtive verdiene i datasettet

#Oppgave E)

start_date <- as.POSIXct("2015-01-01")
 end_date <- as.POSIXct("2015-12-31")
 df_filtered_2015 <- df[df$TIMESTAMP >= start_date & df$TIMESTAMP <= end_date, ]

model <- lm(InvPDC_kW_Avg ~ Pyra1_Wm2_Avg, data = df_filtered_2015)

summary(model)

#Ettersom vi brukte hele året og ikke bare en uke, viser det at modellen ikke er en god modell.  i motsetening om vi tar kun en uke som i de forrige oppgavene virker det som en veldig god modell. Dette ser vi ved bruk av Multiple R squared som ligger på 0.0009301. Men om vi tar tidsperioden 1 juli til 7 juli får vi Multiple R-squared:  0.9787 noe som vi sier at modellen er bra på ukes basis, ikke årsbasis.
