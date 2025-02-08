# Syntaxe des messages de commit

Les messages de commit doivent optimalement suivre une convention claire et standardisée afin de maintenir la lisibilité et la traçabilité du projet. Cette norme est basée sur [Conventional Commits](https://www.conventionalcommits.org/) et vise à clarifier le type de changement, le contexte, et à rendre le développement plus structuré.

## Format général

- **type** : Le type de modification (voir la liste des types ci-dessous).
- **scope** (optionnel) : La partie du projet concernée par le changement (ex. : un service, un module).
- **message** : Une courte description des modifications (en impératif et au présent).

## Types de commits

- **feat** : Ajout d'une nouvelle fonctionnalité.
  - Exemple : `feat(user-auth): add login feature`

- **fix** : Correction d'un bug.
  - Exemple : `fix(payment): resolve rounding issue in invoice calculation`

- **chore** : Tâches mineures n'affectant pas le code applicatif (ex. : mise à jour des dépendances).
  - Exemple : `chore: update dependencies`

- **docs** : Modifications de la documentation.
  - Exemple : `docs(readme): add usage instructions`

- **style** : Changement de style du code (formatage, indentations, etc.) sans impact fonctionnel.
  - Exemple : `style: fix indentation in codebase`

- **refactor** : Refactorisation du code sans changement de comportement.
  - Exemple : `refactor(order-service): simplify method flow`

- **test** : Ajout ou modification de tests.
  - Exemple : `test(user-service): add unit tests`

- **perf** : Améliorations de performance.
  - Exemple : `perf(api): improve database query performance`

- **ci** : Changements liés à l'intégration continue ou aux outils de build.
  - Exemple : `ci: update GitHub Actions configuration`

## Bonnes pratiques

- **Messages clairs et précis** : Le message doit être explicite et ne pas dépasser une ligne. Si des détails supplémentaires sont nécessaires, ils peuvent être inclus dans le corps du commit.
- **Impératif présent** : Utilisez l'impératif au présent pour décrire ce que fait le commit, ex. : « add », « fix », « update ».
- **Scope optionnel** : Le scope est utile pour indiquer la partie du projet impactée par le commit, mais peut être omis si non pertinent.
- **Évitez les termes vagues** : Évitez d'utiliser des termes comme `update`, `change` ou `improve`, qui manquent de précision.

## Exemples de commits

- **Ajout d'une fonctionnalité** :