# CLAUDE.md — Tutorial-Passphrase

## Descripción del Proyecto
Guía completa de passphrase BIP39 para hardware wallets y software wallets de Bitcoin.
Single-page HTML interactivo. Punto de partida: usuario ya tiene wallet operativa.
Cubre activación paso a paso de passphrase en cada dispositivo/app.

## Cómo Ejecutar
Abrir `index.html` en el browser. Desplegado en GitHub Pages.

## Archivos Clave
| Archivo | Responsabilidad |
|---|---|
| `index.html` | Tutorial completo inline (HTML/CSS/JS) |
| `Prints/` | Screenshots de cada wallet (nombrados por sección: hw-jade-01.png, etc.) |
| `Fuentes.txt` | Fuentes oficiales y recursos por dispositivo |
| `CLAUDE.md` | Este archivo |

## Stack
Vanilla HTML/CSS/JS · GitHub Pages · Sin dependencias externas

## Paleta de Colores
- Accent: `#f7931a` (Bitcoin orange)
- Background: `#0f0f0f`
- Surface: `#1a1a1a`
- Text: `#f0f0f0`
- Muted: `#888`

## Bloques del Tutorial
| Grupo | ID en SECTIONS | Wallets cubiertas |
|---|---|---|
| Hardware Wallets | `group: 'hw'` | Jade, Coldcard Q/Mk4/Mk5, BitBox02, Ledger, Trezor, SeedSigner, Passport, Keystone, Specter DIY |
| Desktop Wallets | `group: 'desktop'` | Sparrow, Specter Desktop, Electrum, Blockstream Green |
| Hot Wallets Mobile | `group: 'mobile'` | BlueWallet, Nunchuk, Bull Bitcoin, Blockstream Green, Phoenix |
| Hot Wallets Browser | `group: 'browser'` | Overview (no recomendado para BTC + passphrase) |

## Convención de Nombrado de Prints
```
hw-{device}-{nn}.png     → hardware wallets
sw-{wallet}-{nn}.png     → desktop/software wallets
mob-{wallet}-{nn}.png    → mobile hot wallets
br-{wallet}-{nn}.png     → browser wallets
```
Ejemplos: `hw-jade-01.png`, `sw-sparrow-01.png`, `mob-blue-01.png`

## Datos Clave por Dispositivo (fuente: investigación agentes)
- **Jade**: prompt configurable (Disabled / Next Login Only / Always Ask) + método WordList
- **Coldcard Q**: teclado QWERTY físico completo · fingerprint 8 chars hex · MicroSD AES-256 opcional
- **BitBox02**: passphrase se ingresa SOLO en el dispositivo, nunca en la app
- **Ledger**: 2 modos (Temporary / Attach to PIN) · Flex/Stax tienen teclado táctil
- **Trezor**: hasta 50 chars · "Enter on device" recomendado · Safe 7 pantalla 2.5"
- **Passport**: ruta MORE(↑) → Settings → Advanced → Passphrase · indicador visual "P en escudo"
- **Keystone**: máximo 128 chars · no almacena la passphrase en el dispositivo
- **Phoenix**: Lightning-only, NO soporta BIP39 passphrase estándar
- **Muun**: NO soporta BIP39 passphrase (usa Emergency Kit propio)

## Fuentes Principales de Research
- Econoalchemist: https://econoalchemist.github.io/ (mejor guías visuales)
- Arman the Parman: https://armantheparman.com/passphrase/ (multi-dispositivo)
- Plan B Academy: https://planb.academy/tutorials/wallet/backup/passphrase-*
- Docs oficiales de cada fabricante (ver Fuentes.txt)

## Convenciones del Código
- Todo el contenido está en el array `SECTIONS[]` en el JS del HTML
- Cada sección tiene `id`, `group`, `brand?`, `es/en` (título), y `steps[]`
- Cada step tiene `f` (filename en Prints/), `es/en` (título), `des/den` (HTML body)
- `noImg: true` para pasos sin screenshot
- Tips: `<div class="tip">`, Warnings: `<div class="warn">`, Info: `<div class="info">`
- Lightning address: MatheyBTC@getalby.com (FUNDING.yml cuando se cree)
