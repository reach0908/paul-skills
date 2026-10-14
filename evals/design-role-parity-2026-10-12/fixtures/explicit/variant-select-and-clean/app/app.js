import {renderInvoice} from './components/invoice-summary.js';
import {renderVariant} from './variants/versions.js';
import {mountPicker} from './variants/picker.js';
const invoice={name:'10월 이용 명세서',amount:57000};
mountPicker(name=>renderVariant(document.querySelector('#invoice'),invoice,name));
