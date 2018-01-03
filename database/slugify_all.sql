UPDATE ancien SET nom_slug=slugify(nom), prenom_slug=slugify(prenom);
UPDATE entreprise SET slug=slugify(nom);
UPDATE ville SET slug=slugify(nom);
