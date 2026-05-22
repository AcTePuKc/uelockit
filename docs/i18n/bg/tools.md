---
layout: page
title: Инструменти (BG)
permalink: /i18n/bg/tools/
---

<nav class="doc-nav">
  <a href="{{ '/' | relative_url }}">EN</a>
  <a href="{{ '/i18n/bg/' | relative_url }}">BG</a>
  <a href="{{ '/i18n/bg/quickstart/' | relative_url }}">Бърз старт</a>
  <a href="{{ '/i18n/bg/workflow/' | relative_url }}">Работен процес</a>
  <a href="{{ '/iostore-packaging/' | relative_url }}">Packaging</a>
</nav>

# Инструменти

`UELocKit` следва модела „ти си набавяш инструментите“.

Toolkit-ът дава скриптове и документация. Потребителят осигурява локални копия на външните инструменти.

За нормален потребител най-простият mental model е:
- постави нужния source файл в правилната папка
- направи външните инструменти discoverable
- пусни init скрипта
- превеждай
- пусни build скриптовете

## Upstream линкове

- `FModel`
  GitHub: [4sval/FModel](https://github.com/4sval/FModel)
  Releases: [FModel Releases](https://github.com/4sval/FModel/releases)
- `retoc`
  GitHub: [trumank/retoc](https://github.com/trumank/retoc/)
- `UnrealPak`
  Идва с Unreal Engine.
  Reference overview: [UnrealPak overview](https://unrealpak.com/)

## Какво и кога да използваш

### FModel

Използвай FModel, когато искаш:
- да разглеждаш assets визуално
- да виждаш localization-related assets
- да export-ваш contextual JSON или текст, когато е наличен

FModel е полезен главно за discovery и context, не за rebuild на `.locres`.

### retoc

Използвай `retoc`, когато искаш:
- да inspect-ваш или обработваш Unreal game content на IO Store база
- да конвертираш packaging outputs, когато играта очаква `.utoc` и `.ucas`

В този toolkit `retoc` е част от packaging stage-а.

### UnrealLocres

Използвай `UnrealLocres`, когато искаш:
- export или import на `.locres`
- rebuild на преведен `.locres` от CSV

Това е ключовият инструмент за actual localization data round-trip.

### UnrealPak

Използвай `UnrealPak.exe`, когато искаш:
- да създадеш `.pak`, който ще съдържа преведените localization файлове

### Python

Използвай Python, когато искаш:
- да инициализираш translation workspace от source `.locres`
- да конвертираш JSON към CSV
- да конвертираш CSV към JSON
- да валидираш working translation файловете
- да пускаш леки helper скриптове

Препоръчителна версия:
- Python `3.10` или по-нов

Практическо изискване:
- `python` трябва да е достъпен от terminal или PowerShell

Toolkit-ът не инсталира Python вместо потребителя.

Ако Python не е наличен на машината, потребителят трябва сам да си го инсталира.

### PowerShell

Използвай PowerShell, когато искаш:
- да оркестрираш целия build
- да staging-ваш файловете в правилната Unreal folder структура
- да генерираш `.locmeta`
- да извикваш външните инструменти в правилната последователност

### Python build entrypoint

Използвай Python build entrypoint-а, когато искаш:
- по-малко Windows-specific orchestration слой
- скрипт, който е по-лесен за адаптация за CI или automation
- build flow, който не е вързан само за PowerShell

Текущ скрипт:
- [build_locmod.py](../../../tools/build_locmod.py)

## Tool discovery

Скриптовете търсят инструментите в този ред:

1. Explicit parameter
2. Environment variable
3. Локална workspace конвенция

## Environment variables

- `UNREALLOCRES_EXE`
- `UNREALPAK_EXE`
- `RETOC_EXE`

## Config файл

Sample config:
- [UELocKit.sample.config.psd1](../../../config/UELocKit.sample.config.psd1)

Препоръчителен локален pattern:
- копирай го като `config/UELocKit.config.psd1`
- дръж истинския config файл извън version control

## Препоръчителна public-repo политика

- документирай upstream инструментите
- давай линкове към upstream проектите
- не bundle-вай бинарните файлове, освен ако съзнателно не решиш да ги vendor-неш по-късно

## Какво toolkit-ът прави за потребителя

Ако потребителят осигури:
- source `.locres`
- local tool installations
- валиден config или command-line paths

тогава toolkit-ът може:
- да генерира началните working translation файлове
- да rebuild-не преведен `.locres`
- да генерира `.locmeta`
- да build-не `.pak`
- да конвертира или package-не `.utoc` и `.ucas`

Предпочитан translation editing target:
- генерираният JSON working файл

Compatibility target:
- генерираният CSV working файл

Какво не предоставя:
- оригиналните extracted game файлове
- външните binaries
- game-specific reverse engineering извън този workflow

<nav class="doc-nav">
  <a href="{{ '/tools/' | relative_url }}">Read this page in English</a>
  <a href="{{ '/i18n/bg/workflow/' | relative_url }}">Назад: Работен процес</a>
  <a href="{{ '/iostore-packaging/' | relative_url }}">Напред: Packaging</a>
  <a href="https://github.com/AcTePuKc/uelockit">GitHub Repo</a>
</nav>
