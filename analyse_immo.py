import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# 1. IMPORTATION ET VÉRIFICATION DES DONNÉES

df = pd.read_csv(
    "/Users/miryam/Desktop/Projet-Immobilier/data/AmesHousing.csv"
)

print("Dimensions :", df.shape)
print(df.head())
print(df.columns)

df_clean = df.copy()

nb_doublons = df_clean.duplicated().sum()
print("Nombre de doublons :", nb_doublons)

df_clean = df_clean.drop_duplicates()

nb_na = df_clean.isna().sum()
nb_na = nb_na[nb_na > 0].sort_values(ascending=False)

print("\nValeurs manquantes par colonne :")
print(nb_na.to_string())

nb_na_lot_frontage = df_clean["Lot Frontage"].isna().sum()
pct_na_lot_frontage = round(
    nb_na_lot_frontage / len(df_clean) * 100,
    2,
)

print(
    "Pourcentage de valeurs manquantes dans Lot Frontage :",
    pct_na_lot_frontage,
    "%",
)


# 2. ANALYSE DES PRIX

print("\nStatistiques descriptives du prix :")
print(df_clean["SalePrice"].describe())

plt.figure(figsize=(8, 5))
plt.hist(
    df_clean["SalePrice"],
    bins=30,
    edgecolor="black",
)

plt.title("Distribution des prix")
plt.xlabel("Prix de vente en dollars")
plt.ylabel("Nombre de maisons")
plt.savefig("images/distribution_prix.png", bbox_inches="tight")
plt.show()


# 3. PRIX ET SURFACE HABITABLE

plt.figure(figsize=(8, 5))
plt.scatter(
    df_clean["Gr Liv Area"],
    df_clean["SalePrice"],
    alpha=0.5,
)

plt.title("Prix selon la surface habitable")
plt.xlabel("Surface habitable en pieds carrés")
plt.ylabel("Prix de vente en dollars")
plt.savefig("images/prix_surface.png", bbox_inches="tight")
plt.show()

correlation_surface = df_clean["Gr Liv Area"].corr(
    df_clean["SalePrice"]
)

print(
    "Corrélation entre la surface et le prix :",
    round(correlation_surface, 2),
)


# 4. PRIX ET QUALITÉ GÉNÉRALE

prix_par_qualite = (
    df_clean.groupby("Overall Qual")["SalePrice"]
    .mean()
    .round(2)
)

print("\nPrix moyen selon la qualité :")
print(prix_par_qualite)

plt.figure(figsize=(8, 5))
plt.bar(
    prix_par_qualite.index,
    prix_par_qualite.values,
    edgecolor="black",
)

plt.title("Prix moyen selon la qualité générale")
plt.xlabel("Qualité générale de la maison")
plt.ylabel("Prix moyen en dollars")
plt.savefig("images/prix_qualite.png", bbox_inches="tight")
plt.show()

correlation_qualite = df_clean["Overall Qual"].corr(
    df_clean["SalePrice"]
)

print(
    "Corrélation entre la qualité et le prix :",
    round(correlation_qualite, 2),
)


# 5. PRIX ET QUARTIER

prix_par_quartier = (
    df_clean.groupby("Neighborhood")["SalePrice"]
    .median()
    .sort_values()
)

moins_chers = prix_par_quartier.head(10)
plus_chers = prix_par_quartier.tail(10)

print("\nDix quartiers les moins chers :")
print(moins_chers)

print("\nDix quartiers les plus chers :")
print(plus_chers)

plt.figure(figsize=(10, 5))
plt.barh(
    moins_chers.index,
    moins_chers.values,
    color="orange",
)

plt.title("Les 10 quartiers les moins chers")
plt.xlabel("Prix médian en dollars")
plt.ylabel("Quartier")
plt.tight_layout()
plt.savefig("images/quartiers_moins_chers.png", bbox_inches="tight")
plt.show()

plt.figure(figsize=(10, 5))
plt.barh(
    plus_chers.index,
    plus_chers.values,
    color="green",
)

plt.title("Les 10 quartiers les plus chers")
plt.xlabel("Prix médian en dollars")
plt.ylabel("Quartier")
plt.tight_layout()
plt.savefig("images/quartiers_plus_chers.png", bbox_inches="tight")
plt.show()


# 6. PRIX ET ÂGE DE LA MAISON

df_clean["Age maison"] = (
    df_clean["Yr Sold"] - df_clean["Year Built"]
)

plt.figure(figsize=(8, 5))
plt.scatter(
    df_clean["Age maison"],
    df_clean["SalePrice"],
    alpha=0.4,
)

plt.title("Prix selon l'âge de la maison")
plt.xlabel("Âge au moment de la vente")
plt.ylabel("Prix de vente en dollars")
plt.savefig("images/prix_age.png", bbox_inches="tight")
plt.show()

correlation_age = df_clean["Age maison"].corr(
    df_clean["SalePrice"]
)

print(
    "Corrélation entre l'âge et le prix :",
    round(correlation_age, 2),
)


# 7. PRIX ET GARAGE

prix_par_garage = (
    df_clean.groupby("Garage Cars")["SalePrice"]
    .mean()
    .round(2)
)

nombre_par_garage = (
    df_clean["Garage Cars"]
    .value_counts()
    .sort_index()
)

print("\nPrix moyen selon la capacité du garage :")
print(prix_par_garage)

print("\nNombre de maisons selon la capacité du garage :")
print(nombre_par_garage)


# 8. PRIX ET ANCIENNETÉ DE LA RÉNOVATION

df_clean["Age rénovation"] = (
    df_clean["Yr Sold"] - df_clean["Year Remod/Add"]
)

correlation_renovation = df_clean["Age rénovation"].corr(
    df_clean["SalePrice"]
)

print(
    "Corrélation entre l'ancienneté de la rénovation et le prix :",
    round(correlation_renovation, 2),
)


# 9. TABLEAU RÉCAPITULATIF DES CORRÉLATIONS

resume = pd.DataFrame(
    {
        "Facteur": [
            "Qualité générale",
            "Surface habitable",
            "Âge de la maison",
            "Ancienneté de la rénovation",
            "Capacité du garage",
        ],
        "Corrélation": [
            correlation_qualite,
            correlation_surface,
            correlation_age,
            correlation_renovation,
            df_clean["Garage Cars"].corr(df_clean["SalePrice"]),
        ],
    }
)

resume["Corrélation"] = resume["Corrélation"].round(2)

print("\nRésumé des corrélations :")
print(resume)


# 10. RÉGRESSION LINÉAIRE

x = df_clean["Gr Liv Area"]
y = df_clean["SalePrice"]

modele = np.polyfit(x, y, 1)
prix_estime = modele[0] * x + modele[1]

ordre = np.argsort(x)

plt.figure(figsize=(8, 5))
plt.scatter(x, y, alpha=0.4)
plt.plot(
    x.iloc[ordre],
    prix_estime.iloc[ordre],
    color="red",
)

plt.title("Évolution du prix selon la surface")
plt.xlabel("Surface habitable")
plt.ylabel("Prix de vente")
plt.savefig("images/regression_lineaire.png", bbox_inches="tight")
plt.show()


e_hat = y - prix_estime
std_e_hat = np.std(e_hat, ddof=1)

print(
    "Écart-type des résidus linéaires :",
    round(std_e_hat, 2),
)

plt.figure(figsize=(8, 5))
plt.hist(
    e_hat,
    bins=30,
    edgecolor="black",
)

plt.title("Histogramme des résidus linéaires")
plt.xlabel("Résidus")
plt.ylabel("Effectif")
plt.savefig("images/histogramme_residus_lineaires.png", bbox_inches="tight")
plt.show()

plt.figure(figsize=(6, 5))
plt.boxplot(e_hat)
plt.title("Boîte à moustaches des résidus linéaires")
plt.ylabel("Résidus")
plt.savefig("images/boite_residus_lineaires.png", bbox_inches="tight")
plt.show()

plt.figure(figsize=(8, 5))
plt.scatter(y, e_hat, alpha=0.4)
plt.axhline(0, color="black")
plt.axhline(
    2 * std_e_hat,
    color="red",
    linestyle="--",
)
plt.axhline(
    -2 * std_e_hat,
    color="red",
    linestyle="--",
)

plt.title("Résidus du modèle linéaire")
plt.xlabel("Prix réel")
plt.ylabel("Résidus")
plt.savefig("images/residus_lineaires.png", bbox_inches="tight")
plt.show()

somme_residus = np.sum(e_hat**2)
somme_totale = np.sum((y - y.mean()) ** 2)
R2 = 1 - somme_residus / somme_totale

print("R² linéaire :", round(R2, 2))


# 11. RÉGRESSION POLYNOMIALE DE DEGRÉ 2

modele_p2 = np.polyfit(x, y, 2)

prix_estime_p2 = (
    modele_p2[0] * x**2
    + modele_p2[1] * x
    + modele_p2[2]
)

plt.figure(figsize=(8, 5))
plt.scatter(x, y, alpha=0.4)
plt.plot(
    x.iloc[ordre],
    prix_estime_p2.iloc[ordre],
    color="red",
)

plt.title("Régression polynomiale du prix selon la surface")
plt.xlabel("Surface habitable")
plt.ylabel("Prix de vente")
plt.savefig("images/regression_polynomiale.png", bbox_inches="tight")
plt.show()


e_hat_p2 = y - prix_estime_p2
std_e_hat_p2 = np.std(e_hat_p2, ddof=1)

somme_residus_p2 = np.sum(e_hat_p2**2)
R2_p2 = 1 - somme_residus_p2 / somme_totale

print(
    "Écart-type des résidus polynomiaux :",
    round(std_e_hat_p2, 2),
)
print("R² linéaire :", round(R2, 2))
print("R² polynomial :", round(R2_p2, 2))

plt.figure(figsize=(8, 5))
plt.hist(
    e_hat_p2,
    bins=30,
    edgecolor="black",
)

plt.title("Histogramme des résidus polynomiaux")
plt.xlabel("Résidus")
plt.ylabel("Effectif")
plt.savefig("images/histogramme_residus_polynomiaux.png", bbox_inches="tight")
plt.show()

plt.figure(figsize=(8, 5))
plt.scatter(y, e_hat_p2, alpha=0.4)
plt.axhline(0, color="black")
plt.axhline(
    2 * std_e_hat_p2,
    color="red",
    linestyle="--",
)
plt.axhline(
    -2 * std_e_hat_p2,
    color="red",
    linestyle="--",
)

plt.title("Résidus du modèle polynomial")
plt.xlabel("Prix réel")
plt.ylabel("Résidus")
plt.savefig("images/residus_polynomiaux.png", bbox_inches="tight")
plt.show()
