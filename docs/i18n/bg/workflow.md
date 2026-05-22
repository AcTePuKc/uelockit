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
  <a href="{{ '/iostore-packaging/' | relative_url }}">Packaging</a>
</nav>

# Работен процес

## Общ поток

1. Набавяш source localization файловете от игра, която имаш право да inspect-ваш за modding или personal translation use.
2. Преглеждаш или export-ваш localization данните с предпочитаните от теб инструменти.
3. Копираш extracted source файловете в `source/`.
4. Инициализираш workspace-а от source `.locres`.
5. Държиш extracted `Game.json` в `source/` за бъдещи patch сравнения.
6. Превеждаш `target` текста, без да чупиш keys и placeholders.
7. Изграждаш наново преведения `.locres`.
8. Генерираш `.locmeta`.
9. Пакетираш резултата в `.pak`.
10. Конвертираш или пакетираш до `.utoc` и `.ucas`, ако играта използва IO Store.
11. Тестваш в играта.
12. Повтаряш за playtest fixes и терминологично изглаждане.

## Препоръчани работни файлове

- `working/<target>.<culture>.json`
- `working/<target>.<culture>.csv`
- `working/<target>.en.csv`

Пример:
- `working/Game.bg.json`
- `working/Game.bg.csv`
- `working/Game.en.csv`

Често срещан extracted source пример:
- `Output/.../en/Game.locres`
- `Output/.../en/Game.json`

Често срещана локална working конвенция в `UELocKit`:
- `source/Game.en.locres`
- `source/Game.en.json`

Предпочитан editing файл:
- редактирай `working/<target>.<culture>.json`

Compatibility файл:
- `working/<target>.<culture>.csv` съществува за import/export compatibility, не защото е предпочитаният editing формат

## Избор на output culture

Потребителят избира culture чрез две стойности:

- `CultureTag`
  Използва се във working filenames и обикновено в името на localization папката
- `CultureCode`
  Използва се при генериране на `.locmeta`

Примери:
- `bg` и `bg-BG`
- `pl` и `pl-PL`
- `th` и `th-TH`

Най-лесното място за настройване е:
- `config/UELocKit.config.psd1`

Важно:
- `LocalizationTargetName` обикновено е името на localization файла, не заглавието на играта
- при много игри остава `Game`
- ако го смениш грешно, скриптовете ще търсят грешните файлове

## Правила за редакция

- Не променяй localization keys, освен ако не знаеш много добре защо.
- Не променяй source текста, освен ако съзнателно не поправяш своя working copy.
- Запазвай placeholders като `[InventoryActionPrimary]`.
- Запазвай смислените line breaks.
- Предпочитай JSON за multiline текст и тежки narrative записи.

## Команди за конвертиране

JSON към CSV:

```powershell
python .\tools\translation_io.py json-to-csv `
  --input .\working\Game.bg.json `
  --output .\working\Game.bg.csv
```

CSV към JSON:

```powershell
python .\tools\translation_io.py csv-to-json `
  --input .\working\Game.bg.csv `
  --output .\working\Game.bg.json
```

## Инициализация на workspace-а

Ако потребителят започва само със source `.locres`, `UELocKit` може да генерира началните working файлове.

Пример:

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

Това е bootstrap стъпката преди нормалната работа по превода.

## Проверка при patch update

Когато играта се обнови, extract-ни отново новия source `Game.json` и го копирай в `source/`.

После го сравни с текущия working translation файл:

```powershell
python .\tools\check_source_update.py `
  --working .\working\Game.bg.json `
  --source-json .\source\Game.en.json
```

Това ти дава бърз отчет за:
- добавени keys
- премахнати keys
- променени source стойности

Това е най-безопасният начин да разбереш дали нов patch наистина е променил localizable текстовете, преди да build-ваш отново или да продължиш с превода.

## Команди за build

Изграждане на `.locres`:

```powershell
& .\build-locres.ps1 `
  -ConfigPath .\config\UELocKit.config.psd1 `
  -TranslationFormat json
```

Изграждане на standalone package:

```powershell
& .\tools\build-standalone-locmod.ps1 `
  -ConfigPath .\config\UELocKit.config.psd1 `
  -TranslationFormat json
```

Изграждане без автоматичен deploy:

```powershell
& .\tools\build-standalone-locmod.ps1 `
  -ConfigPath .\config\UELocKit.config.psd1 `
  -TranslationFormat json `
  -DeployToGame $false
```

<nav class="doc-nav">
  <a href="{{ '/workflow/' | relative_url }}">Read this page in English</a>
  <a href="{{ '/i18n/bg/quickstart/' | relative_url }}">Назад: Бърз старт</a>
  <a href="{{ '/i18n/bg/tools/' | relative_url }}">Напред: Инструменти</a>
  <a href="https://github.com/AcTePuKc/uelockit">GitHub Repo</a>
</nav>
