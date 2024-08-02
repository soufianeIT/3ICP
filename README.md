# Dice Game Application

Bienvenue dans l'application Dice Game ! Ce projet propose un jeu de dés avec deux interfaces principales : une interface web pour les joueurs et une interface d'administration pour les gestionnaires.

## Sommaire

1. [Description](#description)
2. [Environnement](#environnement)
3. [Langages](#langages)
4. [Prérequis](#prérequis)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Exécution](#exécution)
8. [Utilisation](#utilisation)
9. [Tests](#tests)
10. [Dépannage](#dépannage)

## Description

L'application Dice Game se compose de deux parties :
- **Interface Web** : Permet aux utilisateurs de jouer au jeu de dés.
- **Interface d'Administration** : Permet aux administrateurs de gérer les utilisateurs, les sessions de jeu, et les configurations.

## Environnement

L'application utilise Docker pour la conteneurisation des services. Les services sont définis dans un fichier `docker-compose.yml`.

## Langages

- **Interface Web** : JavaScript (Node.js, Sequelize)
- **Interface d'Administration** : Python (Flask, SQLAlchemy)
- **Base de données** : MySQL

## Prérequis

Avant de commencer, assurez-vous d'avoir les outils suivants installés sur votre machine :
- Docker
- Docker Compose

## Installation

1. Clonez le dépôt GitHub :
    ```sh
    git clone https://github.com/votre-utilisateur/dice-game.git
    cd dice-game
    ```

2. (Optionnel) Créez un fichier `.env` si vous avez des variables d'environnement spécifiques à définir.

## Configuration

Vérifiez et ajustez le fichier `docker-compose.yml` selon vos besoins. Voici un exemple de configuration :

```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: ./web/Dockerfile
    ports:
      - "4000:4000"
    environment:
      - NODE_ENV=development
      - DB_USER=root
      - DB_PASSWORD=password
      - DB_NAME=dice_game
      - DB_NAME_TEST=dice_game_test
      - DB_HOST=db
    depends_on:
      - db
  
  admin:
    build:
      context: .
      dockerfile: ./admin/Dockerfile
    ports:
      - "5000:5000"
    environment:
      - SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:password@db/dice_game
    depends_on:
      - db

  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: dice_game
      MYSQL_DATABASE_TEST: dice_game_test
    ports:
      - "3306:3306"
    volumes:
      - db-data:/var/lib/mysql

volumes:
  db-data:
