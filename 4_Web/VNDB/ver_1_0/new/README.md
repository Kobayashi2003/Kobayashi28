- app/
  - (main)/
    - (home)/page.tsx
    - [type]/
      - [id]/page.tsx
      - page.tsx
    - user/
      - categories/page.tsx
      - info/page.tsx
      - layout.tsx
    - about/page.tsx
  - layout.tsx
  - favicon.ico
  - globals.css
  - icons.css

- components
  - button/
    - AddButton.tsx
    - BackButton.tsx
    - CancelButton.tsx
    - CardTypeButton.tsx
    - DeleteButton.tsx
    - DeleteModeButton.tsx
    - GhostButton.tsx
    - IconButton.tsx
    - LetterButton.tsx
    - LoginButton.tsx
    - LogoutButton.tsx
    - MarkButton.tsx (TODO)
    - OrderButton.tsx
    - PaginationButtons.tsx
    - RegisterButton.tsx
    - ReloadButton.tsx
    - SubmitButton.tsx
    - TogglePanelButton.tsx
  - card/
    - CardsGrid.tsx
    - ImageCard.tsx
    - TextCard.tsx
  - category/
  - dialog/
    - ConfirmDialog.tsx
    - FiltersDialog.tsx
    - LoginDialog.tsx
    - MarkDialog.tsx (TODO)
    - RegisterDialog.tsx
    - SortByDialog.tsx
  - header/
    - Header.tsx
    - SearchHeader.tsx
    - UserHeader.tsx
  - input/
    - InputBar.tsx
    - SearchBar.tsx
  - panel/
  - selector/
    - LevelSelector.tsx
    - SexualLevelSelector.tsx
    - ViolenceLevelSelector.tsx
  - status/
    - Error.tsx
    - Loading.tsx
    - NotFound.tsx
  - ui/...

- context/
  - UserContext.tsx
  - SearchContext.tsx

- hooks/
  - useHideOnScroll.tsx

- lib/
  - api.ts
  - constants.ts
  - enums.ts
  - icons.ts
  - types.ts
  - utils.ts

- public/
  - icons.png
  - icons.svg

.env.local
middleware.ts
next.config.ts
