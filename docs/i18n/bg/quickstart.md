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
  <a href="{{ '/iostore-packaging/' | relative_url }}">Packaging</a>
</nav>

# Бърз старт

Това е най-краткият път от source `.locres` до workspace, от който можеш да изградиш работещ localization мод.

Изисквания:
- Python `3.10` или по-нов
- PowerShell
- `UnrealLocres`
- `UnrealPak`
- `retoc`, ако играта използва IO Store

## 1. Извлечи или намери source localization файловете

Използвай предпочитания от теб инструмент, за да получиш source localization файловете от играта.

Най-често това са:
- `Game.locres`
- `Game.json`

Ако използваш FModel, може да получиш път от типа:
- `Output/.../en/Game.locres`
- `Output/.../en/Game.json`

Това е нормално.

Source езикът не е задължително да е английски. Ако workflow-ът ти стъпва върху друг вече съществуващ език, можеш да ползваш него.

За default Unreal-style setup в този toolkit най-лесната конвенция е да копираш или посочиш файловете така:
- `source/Game.en.locres`
- `source/Game.en.json`
- `source/Game.fr.locres`
- `source/Game.fr.json`

Ако проектът ти използва друго localization target име, отрази го в config-а.

## 2. Подреди файловете в правилните папки

В `UELocKit` идеята е проста:
- `source/` държи извлечените оригинални файлове от играта
- `working/` държи editable работните файлове за превод

Постави в workspace-а:
- source `.locres`
- source `Game.json`
- външните инструменти някъде на машината си

Не е задължително всички инструменти да са вътре в repo папката, ако предпочиташ environment variables или explicit paths.

## 3. Избери езика

Има две важни стойности:

- `CultureTag`
  Кратък таг за файлове и папки
  Пример: `bg`, `pl`, `th`
- `CultureCode`
  Пълният Unreal culture code за `locmeta`
  Пример: `bg-BG`, `pl-PL`, `th-TH`

Настрой ги в:
- `config/UELocKit.config.psd1`

Започни от:
- `config/UELocKit.sample.config.psd1`

и го копирай като:
- `config/UELocKit.config.psd1`

После редактирай:
- `CultureFolder`
- `CultureCode`
- `LocalizationTargetName`
- `GameName`
- tool paths, ако е нужно

Важно:
- `LocalizationTargetName` обикновено е името на localization target файла, не името на играта
- при много игри трябва да остане `Game`
- не го променяй, освен ако extracted localization файловете ти ясно не използват друго target име

## 4. Направи инструментите откриваеми

Имаш три варианта:

1. Да сложиш инструментите в очакваните локални места
2. Да настроиш environment variables
3. Да подадеш explicit paths към скриптовете

Поддържани environment variables:
- `UNREALLOCRES_EXE`
- `UNREALPAK_EXE`
- `RETOC_EXE`

Python изискване:
- Python `3.10` или по-нов
- `python` трябва да работи от терминал, преди да продължиш

`UELocKit` не инсталира Python автоматично.

## 5. Инициализирай workspace-а

Най-лесната команда за Windows:

```powershell
& .\tools\init_workspace.ps1
```

Тази команда приема, че source файлът следва default конвенцията:
- `source/Game.en.locres`

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

Имената зависят от target името и culture tag-а.

Ако имаш и extracted source JSON, дръж го в `source/`.

Това ти дава лесен начин да сравняваш future game updates срещу текущия working translation файл.

## 6. Превеждай

Редактирай генерирания JSON working файл.

Това е основният файл, по който трябва да работи преводачът.

CSV файлът съществува за compatibility и import/export workflow, но препоръчителният editing формат е JSON.

Пример:
- `working/Game.bg.json`

Ако предпочиташ да работиш в CSV, можеш.

Пример:
- `working/Game.bg.csv`

Можеш да конвертираш между двата формата по всяко време:

```powershell
python .\tools\translation_io.py json-to-csv `
  --input .\working\Game.bg.json `
  --output .\working\Game.bg.csv
```

```powershell
python .\tools\translation_io.py csv-to-json `
  --input .\working\Game.bg.csv `
  --output .\working\Game.bg.json
```

## 7. Провери за промени след update на играта

Когато излезе patch, extract-ни новия source `Game.json` и го копирай в `source/`.

После го сравни с текущия working translation файл:

```powershell
python .\tools\check_source_update.py `
  --working .\working\Game.bg.json `
  --source-json .\source\Game.en.json
```

Това ще ти покаже:
- нови keys
- премахнати keys
- променени source стойности

Ако няма промени, можеш спокойно да продължиш в същия workspace.

## 8. Изгради преведения locres

```powershell
& .\build-locres.ps1 `
  -ConfigPath .\config\UELocKit.config.psd1 `
  -TranslationFormat json
```

## 9. Изгради мод пакета

```powershell
& .\tools\build-standalone-locmod.ps1 `
  -ConfigPath .\config\UELocKit.config.psd1 `
  -TranslationFormat json
```

Това генерира:
- преведен `.locres`
- `.locmeta`
- `.pak`
- `.utoc`
- `.ucas`

## 10. За името на output пакета

Името на output пакета е configurable.

В повечето случаи точният filename не е най-важното. По-важно е:
- да е уникален
- да не се блъска с друг мод
- да следва naming convention-а, който работи най-добре за целевата игра или общността

В зависимост от играта често срещаните pattern-и може да изглеждат така:
- `MyGame-LocMod_P`
- `MyGame-BG_P`
- `pakchunk9999-Localization-Windows_P`

Toolkit-ът по подразбиране използва нещо като:
- `MyUnrealGame-LocMod_P`

Можеш да го промениш в:
- `config/UELocKit.config.psd1`

Ако конкретна игра се окаже чувствителна към load order, chunk naming или platform suffix convention-и, документирай това отделно за тази игра и го следвай там.

## Важна бележка

`UELocKit` не предоставя:
- game файловете ти
- extracted source localization файловете ти
- bundled third-party инструменти

Ти сам трябва да си ги осигуриш.

<nav class="doc-nav">
  <a href="{{ '/quickstart/' | relative_url }}">Read this page in English</a>
  <a href="{{ '/i18n/bg/' | relative_url }}">Назад: Начало</a>
  <a href="{{ '/i18n/bg/workflow/' | relative_url }}">Напред: Работен процес</a>
</nav>
