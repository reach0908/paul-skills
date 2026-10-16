import {CreatorCard as TopicCard} from "./components/TopicCard.js";
import {CreatorCard as RecommendedCard} from "./components/RecommendedCard.js";
const page=new URLSearchParams(location.search).get("page")||"library";
const root=document.querySelector("#app");
const topics=[{id:"design",name:"Design",count:12},{id:"science",name:"Science",count:8}];
if(page==="library"){root.innerHTML=`<h1>Library</h1><section id="recommendations"><h2>Recommended writers</h2></section><section id="topics"><h2>Explore topics</h2></section>`;root.querySelector("#recommendations").append(RecommendedCard({name:"Morgan"}));topics.forEach(t=>root.querySelector("#topics").append(TopicCard(t)));}
else if(page==="collection"){root.innerHTML=`<h1>Collection</h1><p>Your reading list.</p><section id="related"><h2>Related topics</h2><ul><li>Design</li><li>Science</li></ul></section>`;}
else{root.innerHTML=`<h1>Topic</h1><p>${new URLSearchParams(location.search).get("id")}</p>`;}
