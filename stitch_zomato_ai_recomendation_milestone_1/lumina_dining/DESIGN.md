---
name: Lumina Dining
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#5b403f'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#8f6f6e'
  outline-variant: '#e4bebc'
  surface-tint: '#bb162c'
  primary: '#b7122a'
  on-primary: '#ffffff'
  primary-container: '#db313f'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb3b1'
  secondary: '#9d3f49'
  on-secondary: '#ffffff'
  secondary-container: '#ff8c94'
  on-secondary-container: '#77232e'
  tertiary: '#5d5c5b'
  on-tertiary: '#ffffff'
  tertiary-container: '#757474'
  on-tertiary-container: '#f7feff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#ffdada'
  secondary-fixed-dim: '#ffb3b6'
  on-secondary-fixed: '#40000c'
  on-secondary-fixed-variant: '#7e2833'
  tertiary-fixed: '#e5e2e1'
  tertiary-fixed-dim: '#c8c6c5'
  on-tertiary-fixed: '#1c1b1b'
  on-tertiary-fixed-variant: '#474746'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  display-lg:
    fontFamily: Outfit
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-md:
    fontFamily: Outfit
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Outfit
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Outfit
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Outfit
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Outfit
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1280px
  gutter: 24px
  margin-desktop: 64px
  margin-mobile: 20px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style

The design system is engineered to evoke a sense of culinary discovery through an "Atmospheric Premium" lens. It balances the urgency of hunger with the sophistication of AI curation. The target audience is urban food enthusiasts who value both speed and aesthetic quality.

The aesthetic follows a **Refined Glassmorphism** movement. It utilizes frosted-glass surfaces and high-definition background blurs to create depth without clutter. The interface feels lightweight and breathable, using translucent layers to maintain a connection to the rich food photography beneath the UI. Contrast is used strategically—pairing sharp, high-contrast typography with soft, ethereal containers—to ensure the AI recommendations feel both magical and authoritative.

## Colors

The palette is anchored by a vibrant crimson/coral, used exclusively for primary actions, status indicators (like "Open Now"), and AI "sparkle" highlights. 

- **Primary (#E23744):** High-energy red for conversion and brand presence.
- **Secondary (#FF8C94):** A soft tint used for subtle hover states and secondary AI accents.
- **Surface & Backgrounds:** The system uses a "Pure White" (#FFFFFF) for base layers and "Off-White" (#F8F9FA) for section differentiation. 
- **Dark Neutral (#1A1A1A):** Used for primary text and heavy contrast elements to ensure legibility against the vibrant primary color.
- **Glass Tint:** Semi-transparent whites (e.g., `rgba(255, 255, 255, 0.7)`) are used for elevated containers to achieve the glassmorphic effect.

## Typography

The design system utilizes **Outfit** for all levels to leverage its geometric clarity and modern, friendly proportions. 

- **Display & Headlines:** Use tight letter-spacing and bold weights to command attention. These levels are the "voice" of the AI.
- **Body Text:** Set with generous line height to ensure readability of restaurant descriptions and reviews.
- **Labels:** Use a medium weight for buttons and metadata (price ranges, cuisine types) to ensure they stand out even at small sizes.
- **Hierarchical Contrast:** Use color (Primary Red vs. Dark Gray) rather than just size to distinguish between AI-curated insights and standard restaurant data.

## Layout & Spacing

This design system follows a **Fluid Grid** model with a maximum container width for readability on ultra-wide displays.

- **Desktop (1200px+):** A 12-column grid with 24px gutters. Side margins are expansive (64px) to emphasize the premium, airy feel.
- **Tablet (768px - 1199px):** Transitions to an 8-column grid with 20px gutters. Margins reduce to 32px.
- **Mobile (Up to 767px):** A 4-column grid with 16px gutters. Padding is tightened to maximize space for food imagery.

**Spacing Rhythm:** All spacing follows an 8px base unit. Component internal padding should favor `stack-md` (16px) for standard elements and `stack-lg` (32px) for hero cards to maintain a spacious, luxury feel.

## Elevation & Depth

Hierarchy is established through **Glassmorphism and Ambient Shadows**:

1.  **Level 0 (Background):** Neutral light gray (#F8F9FA) or full-bleed food photography.
2.  **Level 1 (Standard Cards):** Solid White (#FFFFFF) with a very soft, diffused shadow (`0 8px 30px rgba(0,0,0,0.04)`).
3.  **Level 2 (AI Recommendations):** Semi-transparent white (`rgba(255, 255, 255, 0.8)`) with a `backdrop-filter: blur(12px)`. These panels have a thin 1px border of `rgba(255,255,255,0.5)` to simulate the edge of glass.
4.  **Level 3 (Overlays/Modals):** High-blur background (`20px`) with a more pronounced shadow.

Shadows are never pure black; they are slightly tinted with the primary red color at 2% opacity to keep the UI "warm."

## Shapes

The shape language is generous and organic. Consistent rounding is used to soften the high-contrast color palette.

- **Standard Elements:** 16px (`rounded-lg`) is the baseline for restaurant cards, input fields, and modals.
- **Interactive Elements:** Buttons and tags use a full **Pill-shape** (`rounded-full`) to encourage interaction and touch-friendliness.
- **Image Containers:** Always follow the container's corner radius. For nested images (e.g., a dish photo inside a card), use a slightly smaller radius (12px) to maintain visual harmony.

## Components

### Buttons & Controls
- **Primary Action:** Pill-shaped, Primary Red background, white text. Bold weight.
- **Segmented Controls:** Housed in a glassmorphic container with a sliding white pill to indicate the active selection.
- **Interactive Sliders:** Used for price and distance. Use a thick track and a large, Primary Red thumb for tactile feedback.

### Cards
- **Restaurant Cards:** Feature a high-aspect-ratio image at the top. The bottom information area uses Level 1 elevation. Metadata (rating, distance) is placed in the top right corner of the image as a glassmorphic tag.
- **AI Recommendation Cards:** Distinguished by a subtle gradient border (Primary Red to Secondary Pink) and a "Sparkle" icon in the top left.

### AI Callouts
- Panels that provide AI "Why you'll like this" insights. These must use the Level 2 glassmorphic styling with a blur effect. Text inside should be `title-md` for the header and `body-md` for the rationale.

### Input Fields
- Search bars should be oversized with a 24px height and 24px horizontal padding. Use a subtle glassmorphic effect when placed over imagery, or a soft gray border when on white backgrounds.

### Lists & Chips
- **Cuisine Chips:** Pill-shaped, light gray background, dark text. On hover, they transition to a Primary Red outline.
- **Lists:** Used for menu items. High-contrast labels with clear price alignment. Use a 1px soft-gray separator.