function answer(elem) {
    answer_id = elem.getAttribute("data-id");
    var url = new URL(document.location.href);
    url.pathname='test/answer';
    (async () => {
        const rawResponse = await fetch(url,{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({answer_id: answer_id})
        });
        const content = await rawResponse.json();
        console.log(content);
        if(content['weight']===100){
            elem.style.color="green";
        }else if (content['weight'] ===0) {
            elem.style.color="gray";
        }
    })();
}
    
    // const answer=fetch('/',{
//     method = )
//           .then(response => response.json())
//           .then(function (text) {
//               if (text.weight==100){
//                   d.innerHTML = "Correct!";
//               }else{
//                   d.innerHTML = "Incorrect"}});
// }
