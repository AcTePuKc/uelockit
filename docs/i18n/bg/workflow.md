---
layout: page
title: Работен процес (BG)
permalink: /i18n/bg/workflow/
---

<nav class="doc-nav">
  <a href="{{ '/' | relative_url }}">EN</a>
  <a href="{{ '/i18n/bg/' | relative_url }}">BG</a>
  <a href="{{ '/i18n/bg/quickstart/' | relative_url }}">Бърз старт</a>
  <a href="{{ '/i18n/bg/tools/' | relative_url }}">Инструменти</a>
</nav>

# Работен процес

## Общ поток

1. Набавяш source localization файловете от играта.
2. Преглеждаш или експортваш localization данните.
3. Инициализираш workspace-а от source `.locres`.
4. Превеждаш `target` текста, без да чупиш keys и placeholders.
5. Изграждаш наново преведения `.locres`.
6. Генерираш `.locmeta`.
7. Пакетираш резултата в `.pak`.
8. Конвертираш до `.utoc` и `.ucas`, ако играта използва IO Store.
9. Тестваш в играта.

## Предпочитан работен файл

- редактирай `working/<target>.<culture>.json`

## Съвместимост

- `working/<target>.<culture>.csv` е за import/export съвместимост, не защото е предпочитаният editing формат

<nav class="doc-nav">
  <a href="{{ '/i18n/bg/quickstart/' | relative_url }}">Назад: Бърз старт</a>
  <a href="{{ '/i18n/bg/tools/' | relative_url }}">Напред: Инструменти</a>
</nav>
