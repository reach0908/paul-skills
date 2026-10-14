import {renderOrder} from './components/order.js';
export const order={sku:'BOOK-SPRING',quantity:2,gift:false,feedback:''};
renderOrder(document.querySelector('#order'),order);
