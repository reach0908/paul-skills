import {renderBooking} from './components/booking-summary.js';
renderBooking(document.querySelector('#booking'));
const rows=[...document.querySelectorAll('.records li')];document.querySelector('#filter').addEventListener('input',e=>rows.forEach(row=>row.hidden=!row.textContent.includes(e.target.value)));
