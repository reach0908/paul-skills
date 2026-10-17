// Creator picker state for mobile onboarding. The view renders `creators` in order
// and restores the list's scroll offset from `scrollTop` after every state change.

export function createState(creators) {
  return { creators, selected: [], scrollTop: 0, version: 0 };
}

export function scrollTo(state, top) {
  return { ...state, scrollTop: top };
}

export function selectCreator(state, id) {
  const selected = state.selected.includes(id)
    ? state.selected.filter((x) => x !== id)
    : [...state.selected, id];
  return reload({ ...state, selected });
}

// Rebuilds the list so selected creators sort first, keeping the reader's place.
function reload(state) {
  const creators = [...state.creators].sort(
    (a, b) => Number(state.selected.includes(b.id)) - Number(state.selected.includes(a.id)),
  );
  return { ...state, creators, version: state.version + 1 };
}
