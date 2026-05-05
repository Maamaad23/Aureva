# Landing Page Quality Report — AUREVA Freight
Generated: 2026-05-05 | URL: https://aurevafreight.com/

---

## Landing Page Health Score

```
Message Match:    ███████░░░  70/100
Page Speed:       ████░░░░░░  42/100  ← CRITICAL
Mobile:           ███████░░░  75/100
Trust Signals:    ██████░░░░  65/100
Form Quality:     █████░░░░░  50/100

Overall:  ██████░░░░  61/100 — Grade C
```

*Formula: (70×0.25) + (42×0.25) + (75×0.20) + (65×0.15) + (50×0.15) = 61*

---

## 1. Message Match — 70/100

**Assessment: Partial match**

The page works well as a general B2B landing page for funeral directors, but lacks ad-specific keyword landing capability.

| Element | Status | Detail |
|---------|--------|--------|
| H1 match | ✅ Pass | "Le dernier voyage, avec dignité" — brand-aligned, dignified |
| Primary CTA above fold | ✅ Pass | "Soumettre un dossier →" — specific and action-oriented |
| IATA trust signal visible | ✅ Pass | IATA badge in nav + hero kicker |
| Offer clarity | ⚠️ Partial | B2B specialization clear, but no specific offer hook (pricing, SLA) |
| Dynamic keyword insertion | ❌ Fail | Static HTML, no DKI possible |
| Ad-specific landing paths | ❌ Fail | One page for all traffic — no segmented pages by campaign/audience |
| Keyword in first 100 words | ⚠️ Partial | "rapatriement" and "pompes funèbres" appear, but below fold |

**Priority fix**: For LinkedIn/Google campaigns targeting "rapatriement funéraire afrique" or "transit funéraire IATA", the hero H1 is emotional but not keyword-anchored. Consider an anchor variation with the keyword in the hero subtitle.

---

## 2. Page Speed — 42/100 ← CRITICAL

**Assessment: FAIL — image optimization is urgent**

| Asset | Current size | Target | Issue |
|-------|-------------|--------|-------|
| `Embarquement.png` (hero BG) | **2.4 MB** | <200KB | Uncompressed PNG, no WebP |
| `Africa.png` | **2.2 MB** | <150KB | PNG, no WebP |
| `Tarmac.png` | **2.3 MB** | <200KB | PNG, no WebP |
| `Cargo.png` | **2.3 MB** | <150KB | PNG, no WebP |
| `volafrique.png` | **2.1 MB** | <150KB | PNG, no WebP |
| `Fenetre afrique.png` | **1.8 MB** | <120KB | PNG, no WebP |
| `og-image.jpg` | 32KB | 150–300KB | Too small for LinkedIn sharing quality |

**Estimated total page weight: ~20MB+ if all images load** — catastrophic for mobile ad clicks.

**LCP risk**: Hero background is `Embarquement.png` (2.4MB) loaded as a CSS `background-image`. This is:
- Not preloadable with full effectiveness (CSS BG images aren't high-priority fetched)
- Correctly marked with `<link rel="preload">` — good — but uncompressed format negates this

**Scripts**: Plausible (`defer`) — lightweight, good. Google Fonts — preconnected, acceptable.

**Fixes in priority order**:
1. Convert all images to WebP/AVIF: `cwebp -q 82 Embarquement.png -o Embarquement.webp` — expected 85-90% size reduction
2. Use `<picture>` elements with WebP + PNG fallback
3. Add `loading="lazy"` to all below-fold images
4. For hero: switch from CSS background to `<img>` tag with `fetchpriority="high"` for true LCP optimization

---

## 3. Mobile Experience — 75/100

**Assessment: Good — a few remaining gaps**

| Check | Status | Detail |
|-------|--------|--------|
| Burger menu | ✅ Pass | Implemented, animates to X, Escape key closes |
| Mobile overlay nav | ✅ Pass | Full-screen, Fraunces italic links |
| Body font ≥16px | ✅ Pass | Base 16px Karla |
| Sticky CTA | ✅ Pass | Fixed gold button, visible at all times |
| Form fields | ✅ Pass | Full-width on mobile, responsive grid collapses |
| Touch targets | ⚠️ Check | Verify nav-burger (44×44px ✅), form labels need 48px tap areas |
| Phone number `tel:` link | ❌ Fail | `href="tel:+33XXXXXXXXX"` — placeholder not filled |
| No horizontal scroll | ✅ Pass | `overflow-x:hidden` on body |
| CTA above fold mobile | ✅ Pass | Sticky CTA always visible |
| Image loading on 3G | ❌ Fail | 2-2.4MB PNGs will cause 10-15s load on mobile 3G |

---

## 4. Trust Signals — 65/100

**Assessment: Certifications strong, social proof absent**

| Signal | Status |
|--------|--------|
| Logo visible above fold | ✅ Nav logo, 52px |
| IATA certification | ✅ Nav badge + hero kicker + distingué section |
| HUM operator status | ✅ Hero kicker |
| Physical address | ✅ Contact section — 20 rue du Jura, Sausheim |
| Email contact | ✅ support@aurevafreight.com |
| Phone number | ❌ Placeholder only |
| Client testimonials | ❌ None — critical for B2B |
| PF client logos | ❌ None |
| Star ratings / reviews | ❌ None (niche B2B, harder to get) |
| SSL/security badge | N/A | GitHub Pages provides HTTPS automatically |
| Response time commitment | ⚠️ "Priorité urgence islamique" in contact — good but vague |

**Gap**: No social proof whatsoever. For PF directors evaluating a new partner, absence of case studies or named client references is a conversion blocker. Even 1-2 anonymized testimonials ("Un directeur de PF, Île-de-France") would significantly improve conversion.

---

## 5. Form Quality — 50/100

**Assessment: mailto: backend is a conversion risk**

| Check | Status | Detail |
|-------|--------|--------|
| Field count | ⚠️ 6 fields | Prénom, Nom, Société, Email, Téléphone, Message — borderline |
| Submit button text | ✅ Pass | "Envoyer la demande" — specific |
| Inline validation | ⚠️ Partial | Basic HTML5 required, no real-time feedback |
| Backend | ✅ Pass | Formspree AJAX (`/f/mvzlovrr`) — reliable delivery |
| Conversion tracking | ✅ Fixed | `plausible('Contact')` fires on success (hardened) |
| UTM capture | ❌ Fail | No UTM parameter storage |
| Click ID preservation | ❌ Fail | No gclid/fbclid capture |
| Multi-step | N/A | 6 fields is workable in single-step for B2B |
| Thank you state | ✅ Pass | Inline success state shown on submit |

**CRITICAL**: `mailto:` forms have ~30-40% failure rate depending on client config. Many corporate computers (PF directors) have no default mail client configured. Recommend Formspree / Netlify Forms / Resend for reliable delivery + webhook for tracking.

---

## UTM / Attribution

| Check | Status |
|-------|--------|
| UTM parameters captured | ❌ No server-side storage |
| gclid (Google Ads) | ❌ Not captured |
| fbclid (Meta) | ❌ Not captured |
| Plausible analytics | ✅ Configured with `defer` |
| Conversion event fired | ❌ Form success fires no Plausible goal |

Plausible has a simple `plausible('goal-name')` API. Add on form success:
```javascript
if (window.plausible) plausible('Contact Form Submit');
```

---

## Quick Wins (sorted by conversion impact)

| # | Fix | Expected Impact | Effort |
|---|-----|-----------------|--------|
| 1 | **Convert images to WebP** — Embarquement, Africa, Tarmac, Cargo | -80% load time, +15-25% mobile CVR | Medium |
| 2 | **~~Replace mailto: (already Formspree)~~** | ✅ Done | — |
| 3 | **~~Plausible goal on form submit~~** | ✅ Done via harden | — |
| 4 | **Add 1-2 anonymized PF testimonials** | +10-20% conversion for cold traffic | Medium |
| 5 | **Fill phone number placeholder** | Trust signal, click-to-call on mobile | Very low (operational) |
| 6 | **OG image upgrade** (current: 32KB, blurry on LinkedIn) | Better CTR on LinkedIn shares | Medium (blocked by Gemini quota) |

---

## Platform-Specific Notes

| Platform | Assessment |
|----------|-----------|
| **LinkedIn** (primary) | Page fits B2B context ✅. OG image too small for rich preview ❌ |
| **Google Search** | No dynamic keyword insertion capability. One generic landing page for all ad groups ❌ |
| **Email** | `mailto:` is the form backend — circular dependency issue |

---

## Recommended Next Steps

1. `/impeccable harden` — form robustness, error states, backend swap
2. Image optimization sprint — WebP conversion for all Images/
3. Add Plausible form goal (5-min fix)
4. `/banana` — OG image (needs Gemini billing enabled)
