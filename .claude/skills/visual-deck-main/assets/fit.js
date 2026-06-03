/* 等比缩放铺满视口并居中 */
function fit(){
  var s=document.querySelector('.slide');
  s.style.transform='none';
  var k=Math.min(window.innerWidth/s.offsetWidth, window.innerHeight/s.offsetHeight);
  s.style.transform='scale('+k.toFixed(4)+')';
}
window.addEventListener('resize',fit);
window.addEventListener('load',fit);
fit();
