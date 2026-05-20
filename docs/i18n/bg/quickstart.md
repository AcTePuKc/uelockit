---
layout: page
title: Бърз старт (BG)
permalink: /i18n/bg/quickstart/
---

<nav class="doc-nav">
  <a href="{{ '/' | relative_url }}">EN</a>
  <a href="{{ '/i18n/bg/' | relative_url }}">BG</a>
  <a href="{{ '/i18n/bg/workflow/' | relative_url }}">Работен процес</a>
  <a href="{{ '/i18n/bg/tools/' | relative_url }}">Инструменти</a>
</nav>

# Бърз старт

Това е най-краткият път от source `.locres` до работещ translation workspace.

## 1. Извлечи или намери source localization файла

Използвай предпочитания от теб tool, за да получиш source localization файла от играта.

Най-често това е нещо като:
- `Game.locres`

Ако използваш FModel, може да получиш път от типа:
- `Output/.../en/Game.locres`

Това е нормално.

## 2. Избери езика

Има две важни стойности:

- `CultureTag`
  Кратък таг за файлове и папки
  Пример: `bg`, `pl`, `th`
- `CultureCode`
  Пълният Unreal culture code за `locmeta`
  Пример: `bg-BG`, `pl-PL`, `th-TH`

Настрой ги в:
- `config/UELocKit.config.psd1`

## 3. Инициализирай workspace-а

Windows shortcut:

```powershell
& .\tools\init_workspace.ps1
```

Python вариант:

```powershell
python .\tools\init_workspace.py `
  --workspace-root . `
  --source-locres .\source\Game.en.locres `
  --localization-target Game `
  --culture-tag bg
```

Това генерира:
- `working/Game.en.csv`
- `working/Game.bg.csv`
- `working/Game.bg.json`

## 4. Превеждай

Редактирай генерирания JSON working файл.

Това е основният файл, по който трябва да работи преводачът.

## 5. Изгради преведения locres

```powershell
& .\build-locres.ps1 `
  -ConfigPath .\config\UELocKit.config.psd1 `
  -TranslationFormat json
```

## 6. Изгради мод пакета

```powershell
& .\tools\build-standalone-locmod.ps1 `
  -ConfigPath .\config\UELocKit.config.psd1 `
  -TranslationFormat json
```

<nav class="doc-nav">
  <a href="{{ '/i18n/bg/' | relative_url }}">Назад: Начало</a>
  <a href="{{ '/i18n/bg/workflow/' | relative_url }}">Напред: Работен процес</a>
</nav>
