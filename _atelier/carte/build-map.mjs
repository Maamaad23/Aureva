import fs from 'fs';
import { feature } from 'topojson-client';
import { geoAzimuthalEqualArea, geoPath } from 'd3-geo';
const topo = JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-110m.json'));
const all = feature(topo, topo.objects.countries).features;
const R = {
  ouest: [686,270,624,324,694,430,384,288,768,204,566,562,466,854,478,132],
  centre: [120,148,140,226,266,178,180,678,24],
  est: [231,232,262,706,404,800,646,108,834,508,450,174,454,894,716,710,72,516,426,748,728,480,690,729],
  nord: [504,12,788,434,818],
};
const regionOf = {}; for (const [k, ids] of Object.entries(R)) for (const id of ids) regionOf[id] = k;
const W = 600, H = 660;
const proj = geoAzimuthalEqualArea().rotate([-14, -10]).clipExtent([[0,0],[W,H]]);
// cadre : de Dakar/Cap-Vert à Madagascar, du Cap à l'Alsace
const frame = { type: 'MultiPoint', coordinates: [[-24, 15], [51, -12], [20, -35], [8, 50], [-10, 50], [52, 12]] };
proj.fitExtent([[18, 14], [W - 18, H - 14]], frame);
const path = geoPath(proj).digits(1);
const out = { ouest: [], centre: [], est: [], nord: [], afrique: [], monde: [] };
const AFR = new Set([...Object.values(R).flat(), 732, 706]); // + Sahara occidental (neutre)
for (const f of all) {
  const id = +f.id; const b = path.bounds(f);
  if (!isFinite(b[0][0]) || b[1][0] < 0 || b[0][0] > W || b[1][1] < 0 || b[0][1] > H) continue;
  const d = path(f); if (!d) continue;
  const reg = regionOf[id];
  if (reg) out[reg].push(d); else if (AFR.has(id)) out.afrique.push(d); else out.monde.push(d);
}
const P = (ll) => proj([ll[1], ll[0]]).map((v) => +v.toFixed(1));
const CITIES = {
  ouest: [['Abidjan',5.26,-3.93],['Accra',5.6,-0.17],['Bamako',12.53,-7.95],['Banjul',13.34,-16.65],['Bissau',11.89,-15.65],['Conakry',9.58,-13.61],['Cotonou',6.36,2.38],['Dakar',14.67,-17.07],['Lagos',6.58,3.32],['Lomé',6.17,1.25],['Niamey',13.48,2.18],['Nouakchott',18.1,-15.95],['Ouagadougou',12.35,-1.51]],
  centre: [['Bangui',4.4,18.52],['Brazzaville',-4.25,15.25],['Douala',4.01,9.72],['Kinshasa',-4.39,15.44],['Libreville',0.46,9.41],['Malabo',3.76,8.71],["N'Djamena",12.13,15.03]],
  est: [['Addis-Abeba',8.98,38.8],['Antananarivo',-18.8,47.48],['Dar es Salaam',-6.88,39.2],['Djibouti',11.55,43.15],['Johannesburg',-26.14,28.25],['Kigali',-1.97,30.14],['Mayotte',-12.8,45.28],['Moroni',-11.53,43.27],['Nairobi',-1.32,36.93]],
  nord: [['Agadir',30.33,-9.41],['Alger',36.69,3.22],['Annaba',36.82,7.81],['Béjaïa',36.71,5.07],['Casablanca',33.37,-7.59],['Constantine',36.28,6.62],['Djerba',33.87,10.78],['Fès',33.93,-4.98],['Le Caire',30.12,31.41],['Marrakech',31.61,-8.04],['Monastir',35.76,10.75],['Nador',34.99,-3.03],['Oran',35.62,-0.62],['Oujda',34.79,-1.92],['Rabat',34.05,-6.75],['Tanger',35.73,-5.92],['Tlemcen',35.02,-1.46],['Tunis',36.85,10.23]],
};
const DEP = [['BSL',47.59,7.53],['LYS',45.72,5.08],['SXB',48.54,7.63]];
const data = {
  w: W, h: H,
  dep: DEP.map(([c, la, ln]) => [c, ...P([la, ln])]),
  cities: Object.fromEntries(Object.entries(CITIES).map(([k, l]) => [k, l.map(([n, la, ln]) => [n, ...P([la, ln])])])),
};
let svg = `<svg class="dm-svg" viewBox="0 0 ${W} ${H}" role="img" aria-labelledby="dm-t"><title id="dm-t">Carte : départs de France, arrivées dans toute l'Afrique</title>`;
svg += `<path class="dm-world" d="${out.monde.join('')}"/>`;
svg += `<path class="dm-afr" d="${out.afrique.join('')}"/>`;
for (const k of ['ouest','centre','est','nord']) svg += `<path class="dm-reg" data-r="${k}" d="${out[k].join('')}"/>`;
svg += `<g class="dm-routes"></g><g class="dm-dots"></g>`;
svg += data.dep.map(([c, x, y], i) => `<circle class="dm-dep${i ? '' : ' is-base'}" cx="${x}" cy="${y}" r="${i ? 2.6 : 3.6}"/>`).join('');
svg += `</svg>`;
fs.writeFileSync('map.svg', svg);
fs.writeFileSync('map-data.json', JSON.stringify(data));
console.log('svg bytes', svg.length, 'gzip?');
