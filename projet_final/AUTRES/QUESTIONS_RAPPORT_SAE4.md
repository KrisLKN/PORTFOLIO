# Questionnaire pour la Rédaction du Rapport Final SAE 4

Afin de rédiger un rapport parfait, détaillé et unique (qui se démarque vraiment de votre brouillon et du rapport de référence), j'ai besoin de détails croustillants sur votre projet. 
Répondez à ces questions directement dans ce fichier ou dans un autre document, avec le plus de détails possible. Plus vous m'en direz, plus le rapport final sera riche, précis et professionnel.

## 1. Contexte et Organisation
* **La transition Oracle (S3) -> Microsoft (S4)** : Qu'est-ce qui a été le plus difficile dans ce changement (syntaxe T-SQL, SSIS vs ODI, installation) ?
* **Répartition du travail** : Dans votre brouillon, vous avez mis une réparition. Avez-vous des anecdotes sur la collaboration ? Comment vous êtes-vous synchronisés ? (ex: utilisation de GitHub, partage de fichiers, appels Discord etc.)
* **Temps de travail** : Avez-vous passé beaucoup de temps sur une tâche en particulier qui n'était pas prévue ?

## 2. Architecture et Modélisation (Bases de données)
* **Les 7 bases de données** : Pourquoi avoir séparé en 7 bases de données sous SQL Server ? Était-ce une contrainte de la SAE ou un choix de votre part pour mieux simuler des environnements distincts ?
* **Modèle en étoile** : 
    * Avez-vous rencontré des problèmes pour aplatir les tables de Chinook (normalisées) vers le format dimensionnel ?
    * Pourquoi avoir choisi de faire remonter les playlists directement dans `DIM_PISTE` au lieu de faire un flocon (Snowflake) avec une table `DIM_PLAYLIST` séparée ? (C'est un excellent point architectural à justifier).
* **La table Magasin (Store)** : Pouvez-vous donner plus de détails sur le schéma de la base "Magasin" ? Quelles étaient les différences majeures avec "Chinook" qui ont rendu la fusion difficile ?

## 3. Le cœur du réacteur : Le processus ETL avec SSIS
* **DSA (Extraction)** : 
    * Pourquoi avoir choisi un `TRUNCATE` + `INSERT` pour le DSA ? Avez-vous envisagé d'autres méthodes ?
* **ODS (Stockage Opérationnel)** : 
    * Comment avez-vous géré concrètement la détection des lignes nouvelles vs lignes modifiées ? (ex: utilisation du composant Lookup).
    * Pouvez-vous m'expliquer précisément comment fonctionne votre mécanisme anti-doublon ?
* **DWH (Data Warehouse) & SCD Type 2** :
    * C'est la partie la plus importante. Vous avez dit que le SCD2 ne se déclenchait pas au début. Pouvez-vous me raconter comment vous avez fini par résoudre le problème dans le composant **SCD Wizard** ou via des flux personnalisés ? 
    * Avez-vous été obligés de rajouter des valeurs par défaut dans SQL Server (ex: DATE_DEBUT) pour que SSIS fonctionne correctement ?
* **Orchestration** : 
    * L'idée des "packages maîtres" (`00_RUN_ALL...`) est géniale. Comment avez-vous géré l'exécution séquentielle ? Avez-vous configuré des comportements spécifiques si un sous-package échoue (ex: arrêt total ou continuation directe) ?

## 4. Difficultés Techniques et Solutions (Le "vrai" travail d'ingénieur)
* **Les Truncations de chaînes de caractères** : Avez-vous eu des `Warnings` dans SSIS relatifs à la longueur des chaînes (Data truncation, ex: des NVARCHAR(4000) voulant rentrer dans du NVARCHAR(500)) ? Comment les avez-vous résolus (Derived Column avec CAST, modification du schéma SQL) ?
* **Conversions de types** : Avez-vous beaucoup lutté avec les conversions de types entre Oracle/Chinook et SQL Server dans SSIS (`(DT_DBDATE)`, `(DT_I4)`, etc.) ?
* **Performances** : Est-ce que le chargement complet de l'ETL prend du temps ? Avez-vous fait des optimisations (ex: virer des colonnes inutilisées dans les flux) ?

## 5. Perspectives d'amélioration
* Si la SAE durait 2 semaines de plus, quelle fonctionnalité auriez-vous ajoutée en priorité ?
    * L'envoi de mails d'alerte en cas de plantage d'un package ?
    * Le déploiement du DWH sur le Cloud (Azure) ?
    * Un cube multidimensionnel (SSAS) pour accélérer le requêtage de Power BI ?

## 6. Captures d'écran à me fournir (TRES IMPORTANT)
Pourriez-vous prendre ces captures et les mettre dans un dossier (ex: `images_rapport/`) ? C'est ce qui donnera la note maximale à votre rapport.
1. **SSMS** : L'explorateur d'objets montrant vos 7 bases de données.
2. **SSMS** : Une requête `SELECT * FROM DIM_PISTE` montrant 2 lignes pour la même piste (l'ancienne désactivée, la nouvelle avec le nouveau prix et `ACTIF=1`), pour prouver que votre SCD2 marche.
3. **SSIS** : Le *Control Flow* d'un package maître (ex: `00_RUN_ALL...`) montrant toutes les boîtes avec le petit "V" vert de succès.
4. **SSIS** : Le *Data Flow* complet du package qui charge `DIM_PISTE`.
5. **SSIS** : Le *Data Flow* du chargement de la table de faits `FAIT_VENTE` (montrant le `Union All` et les différents `Lookups` pour récupérer les clés techniques).
6. **Modélisation** : Une belle capture de votre schéma en étoile final (DWH) si vous en avez une, sinon je la génèrerai en code.

---
**Instructions pour moi (Antigravity) :**
Une fois que vous m'aurez répondu, je mettrai à jour le brouillon pour créer le fichier LaTeX/Markdown/PDF final parfait.
