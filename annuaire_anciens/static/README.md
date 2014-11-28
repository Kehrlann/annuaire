#Version React+Backbone+Browserify de l'app web

Pour commencer, installer node (npm est dans le bundle) puis télécharger les dépendances en executant :
```
npm install
```


Index.html référence app-bundle.js qui généré à partir des contenus du dossier app/
Pour surveiller la modification des fichiers et mettre à jour le app-bundle.js, executer la ligne suivante :
```
watchify -o app-bundle.js -v -d .
```

Pour comprendre le code, commencer par ouvrir app/Router.js c'est là que sont consignée les routes :
```
routes: {
    "search/:term": "search",
    "search": "search",
    "*actions": "defaultRoute"
},
```
Les routes se lisent de haut en bas, c'est pourquoi la ligne tout en bas est une wildcard.
Les routes se lisent "pattern": "fonction à executer"
ex: si j'ai une route de la forme search/bonjour, executer la méthode search et lui passer "bonjour" en argument.

Les routes sont assez simples et font principalement un render de composant React :
```
React.renderComponent(
  SearchView({term: term}),
  document.getElementById('js-main')
);
```
React.renderComponent(Composant(arguments), DOMNodeARemplir);

La navbar est un composant indépendant des routes, c'est pourquoi il est chargé lors de la méthode initialize, qui est executée une seule fois lors du chargement de l'app.

Pour rajouter des vues, il faut
- rajouter une route dans la liste
- créer un (ou plusieurs) nouveau composant react (prendre search.jsx comme exemple)
- créer une méthode dans le Router pour render le composant adéquat.

J'espère que ces explications suffiront à te permettre d'avancer. Je reste disponible biensur !
