# Cómo contribuir al Tutorial de Passphrase BIP39

¡Gracias por querer mejorar este recurso! Cualquier corrección o aporte es bienvenido.

## Formas de contribuir

### 1. Reportar un error o información desactualizada
Si encontrás algo incorrecto (pasos que cambiaron, screenshots desactualizados, texto confuso):

1. Abrí un [Issue](../../issues/new?template=correccion.md)
2. Indicá el dispositivo/wallet afectado y qué está mal
3. Si podés, adjuntá captura o fuente oficial

### 2. Sugerir una wallet que falta
Si usás una wallet que no está cubierta:

1. Abrí un [Issue](../../issues/new?template=wallet-nueva.md)
2. Indicá nombre de la wallet y enlace a la documentación oficial
3. Si tenés screenshots del proceso, mejor todavía

### 3. Proponer mejoras al texto
Si algo no se entiende o podría explicarse mejor:

1. Abrí un [Issue](../../issues/new?template=mejora.md) describiendo qué mejorarías
2. O directamente hacé un Pull Request con el cambio

---

## Cómo hacer un Pull Request

1. Hacé fork del repo
2. Creá una rama: `git checkout -b fix/ledger-paso-5`
3. Hacé tus cambios en `index.html`
4. Hacé commit: `git commit -m "fix: corrige descripción paso 5 Ledger Nano X"`
5. Abrí un Pull Request describiendo qué cambiaste y por qué

---

## Convenciones

**Nombres de archivos de imágenes:**
```
hw-{device}-{nn}.png     → hardware wallets
sw-{wallet}-{nn}.png     → desktop/software wallets
mob-{wallet}-{nn}.png    → mobile hot wallets
```

**Idioma:** el tutorial es bilingüe (español e inglés). Todo cambio debe incluir ambos idiomas.

**Fuentes:** siempre citá la fuente oficial del fabricante/desarrollador cuando corrijas información técnica.

---

## Código de conducta

Este es un espacio técnico y educativo. Sin spam, sin altcoins, sin precio.
