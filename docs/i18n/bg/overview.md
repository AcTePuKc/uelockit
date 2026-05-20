---
layout: page
title: Общ преглед (BG)
permalink: /i18n/bg/overview/
---

<nav class="doc-nav">
  <a href="{{ '/' | relative_url }}">EN</a>
  <a href="{{ '/i18n/bg/' | relative_url }}">BG</a>
  <a href="{{ '/i18n/bg/quickstart/' | relative_url }}">Бърз старт</a>
  <a href="{{ '/i18n/bg/workflow/' | relative_url }}">Работен процес</a>
  <a href="{{ '/i18n/bg/tools/' | relative_url }}">Инструменти</a>
</nav>

# Общ преглед

`UELocKit` е практичен workflow за превод на вече съществуващи Unreal Engine localization стрингове и публикуването им като localization мод.

## Основна идея

- намираш или извличаш съществуващ `.locres`
- конвертираш го в удобен работен формат
- превеждаш съществуващите стрингове
- изграждаш наново преведен `.locres`
- пакетираш резултата за целевата игра

## Важна граница

`UELocKit` е за работа със съществуващи localization keys, които играта вече използва.

Не приема, че можеш:
- да измислиш чисто нов localization key
- да го инжектираш във всяка Unreal игра
- и играта автоматично да го визуализира

Това е game-specific поведение и не трябва да се обещава от generic toolkit.

<nav class="doc-nav">
  <a href="{{ '/i18n/bg/' | relative_url }}">Назад: Начало</a>
  <a href="{{ '/i18n/bg/quickstart/' | relative_url }}">Напред: Бърз старт</a>
</nav>
