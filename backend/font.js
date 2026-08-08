const res = await fetch("https://fonts.google.com/metadata/fonts");
const json = await res.json();
console.log(json.familyMetadataList.map(f => f.family));