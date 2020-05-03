/*const parallax= document.getElementById
("big");
window.addEventListener("scroll", function()
{
    let offset=window.pageYOffset;
    parallax.style.backgroundPositionY=offset
    * 0.7 +"px";

})
*/


var t1=new TimelineMax({onUpdate:updatePercentage});
const controller=new ScrollMagic.Controller();

t1.from("p", .5, {x:200,opacity:0});
t1.from('#homo1', 1, {x:200, opacity:0});
t1.from('#homo2', 1, {x:200, opacity:0});
const scene=new ScrollMagic.Scene({
    triggerElement:"white",
    triggerHook:"onLeave",
    duration:"100%"
})

.setPin(".white")
.setTween(t1)
 .addTo(controller);

 function updatePercentage() {
 t1.progress();
 console.log(t1.progress());
 }