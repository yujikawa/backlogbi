export function range(start: number, end: number): Array<number> {
  // ex) range(1, 3) return [1,2,3]
  return Array.from({length: (end - start + 1)}, (v, k) => k + start);
}
