---
layout: page
title: Начало (BG)
permalink: /i18n/bg/
---

<nav class="doc-nav">
  <a href="{{ '/' | relative_url }}">EN</a>
  <a href="{{ '/i18n/bg/' | relative_url }}">BG</a>
  <a href="{{ '/i18n/bg/quickstart/' | relative_url }}">Бърз старт</a>
  <a href="{{ '/i18n/bg/workflow/' | relative_url }}">Работен процес</a>
  <a href="{{ '/i18n/bg/tools/' | relative_url }}">Инструменти</a>
</nav>

# UELocKit

`UELocKit` е малък toolkit за създаване на Unreal Engine локализационни модове от вече съществуващи стрингове в играта.

Подходящ е за преводачи и модъри, които искат повтаряем процес за:
- безопасно редактиране на преводи
- повторно изграждане на `.locres`
- генериране на `.locmeta`
- пакетиране на локализационен мод в `.pak`
- конвертиране до `.utoc` и `.ucas`, когато играта използва IO Store

## Започни оттук

- [Общ преглед](./overview.md)
- [Бърз старт](./quickstart.md)
- [Работен процес](./workflow.md)
- [Инструменти](./tools.md)

## Поддържан процес

`UELocKit` поддържа практичен процес, базиран на:
- съществуващ source `.locres`
- работен файл за превод в `json` или `csv`
- генерирани работни файлове от source `.locres`
- повторно изграждане на преведения localization output
- пакетиране за Unreal Engine игри

## Какво не прави

`UELocKit` не се опитва да:
- разпространява оригинални търговски файлове на играта
- разпространява извлечени proprietary localization файлове
- bundle-ва външни инструменти по подразбиране
- гарантира поддръжка за измисляне на чисто нови localization keys във всяка Unreal игра

## Важно

Потребителят сам трябва да си набави:
- извлечените localization входни файлове
- локалните tool инсталации

Репото дава workflow и скриптове. Не разпространява допълнителните файлове от конкретна игра.

<nav class="doc-nav">
  <a href="{{ '/i18n/bg/quickstart/' | relative_url }}">Напред: Бърз старт</a>
</nav>
