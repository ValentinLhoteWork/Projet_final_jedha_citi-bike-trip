# Projet Final : Citi-bike trip
<img width="512" height="512" alt="citi-bike" src="https://github.com/user-attachments/assets/187c9cfc-6087-4657-9c12-bf857500afbb" />

## Data lake S3
<img width="2542" height="515" alt="S3_racine_project_citi-bike" src="https://github.com/user-attachments/assets/682bc17f-8218-4f7b-916e-6136dfc6ba20" />
<img width="2047" height="532" alt="S3_nyc_raw_data_project_citi-bike" src="https://github.com/user-attachments/assets/0d3a0393-a113-45ce-94f6-01d366469c9d" />
<img width="2056" height="441" alt="S3_raw_folder_project_citi-bike" src="https://github.com/user-attachments/assets/b1acc4a5-eafb-4954-b3dc-29daaaefa8c0" />


## Introduction

### Citi Bike est le pilier de la micromobilité à New York et le plus grand réseau de vélos en libre-service d'Amérique du Nord.
### Lancé en mai 2013 avec seulement 6 000 vélos, le système opéré par Lyft a connu une croissance exponentielle pour atteindre une flotte de près de 40 000 vélos répartis sur plus de 2 200 stations à travers NYC, Jersey City et Hoboken.
### En franchissant la barre historique des 300 millions de trajets cumulés et en enregistrant près de 47 millions de trajets par an, Citi Bike s'est imposé comme un transport public de masse à part entière, rivalisant en été avec la fréquentation de lignes ferroviaires entières comme le réseau PATH.

## Objectif

### L’objectif est de prédire le net_flow d’une station Citi Bike à une date et une heure données, à partir de l’historique des flux, des données temporelles, des conditions météorologiques et des caractéristiques des stations.
### Le modèle est entraîné sur l’ensemble des données historiques afin de généraliser les comportements observés et de fournir une prédiction applicable à différentes stations et situations.
### Cette prédiction doit permettre d’anticiper les déséquilibres de disponibilité des vélos et, à terme, d’aider à leur gestion.
