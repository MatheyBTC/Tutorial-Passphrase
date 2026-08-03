# Tutorial Passphrase BIP39

**Guía interactiva para configurar una passphrase BIP39 en las principales wallets Bitcoin.**  
Bilingüe (ES/EN) · Sin dependencias · Una sola página HTML

🔗 **[Ver tutorial en vivo →](https://matheybTC.github.io/Tutorial-Passphrase/)**

---

## ¿Qué es esto?

Una guía paso a paso con capturas de pantalla reales para configurar la **passphrase BIP39** (también llamada "25ta palabra" o "wallet oculta") en hardware wallets, hot wallets mobile y desktop.

Cada wallet tiene su propio flujo con fotos del proceso real, explicaciones claras y el fingerprint de verificación para confirmar que la passphrase fue aplicada correctamente.

---

## Wallets cubiertas

### Hardware Wallets
| Wallet | Estado |
|--------|--------|
| Blockstream Jade | ✅ Disponible |
| Blockstream Jade Plus | ✅ Disponible |
| Coldcard Mk4 | ✅ Disponible |
| Coldcard Mk5 | ✅ Disponible |
| Coldcard Q | ✅ Disponible |
| BitBox02 | ✅ Disponible |
| Ledger Nano X | ✅ Disponible |
| Trezor Model T | ✅ Disponible |
| Trezor Safe 3 | ✅ Disponible |
| Trezor Safe 5 | ✅ Disponible |
| Trezor Safe 7 | ✅ Disponible |
| Foundation Passport Core | ✅ Disponible |
| Trezor One | 🔜 Próximamente |

### Hot Wallets Mobile
| Wallet | Estado |
|--------|--------|
| BlueWallet | ✅ Disponible |
| Bull Bitcoin Wallet | ✅ Disponible |
| Nunchuk | 🔜 Próximamente |

### Software (Companion App)
| Wallet | Estado |
|--------|--------|
| Trezor Suite (Desktop) | ✅ Disponible |
| Trezor Suite (Mobile) | ✅ Disponible |

---

## Características

- **Sin dependencias** — HTML, CSS y JS vanilla. Sin frameworks, sin node_modules
- **Bilingüe** — Español e inglés, toggle en la interfaz
- **Offline-ready** — Funciona sin conexión una vez cargado
- **Fotos reales** — Capturas del proceso en dispositivos físicos
- **Fingerprint de verificación** — Cada tutorial incluye cómo confirmar que la passphrase fue aplicada correctamente

---

## Estructura del proyecto

```
Tutorial-Passphrase/
├── index.html          # App completa (HTML + CSS + JS en un solo archivo)
├── Prints/             # Imágenes de los tutoriales (no incluidas en repo público)
├── scripts/            # Scripts de utilidad para procesamiento de imágenes
├── .github/
│   ├── workflows/      # Deploy automático a GitHub Pages
│   └── ISSUE_TEMPLATE/ # Templates para reportar errores o sugerir wallets
└── CONTRIBUTING.md     # Cómo contribuir
```

---

## Contribuir

¿Encontraste un error? ¿Falta tu wallet? ¿Cambió algún paso?

- **[Reportar un error](../../issues/new?template=correccion.md)**
- **[Sugerir una wallet](../../issues/new?template=wallet-nueva.md)**
- **[Proponer mejora de contenido](../../issues/new?template=mejora.md)**

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para instrucciones de Pull Request.

---

## Aviso

Este tutorial es educativo. La passphrase BIP39 protege tus fondos — **si la perdés, no hay recuperación posible**. Siempre probá con una wallet nueva antes de mover fondos reales.

No hay afiliaciones con ninguna de las marcas mencionadas.

---

*Por [@MatheyBTC](https://x.com/MatheyBTC)*
